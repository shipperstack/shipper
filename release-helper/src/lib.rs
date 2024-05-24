use anyhow::{anyhow, Error};
use chrono::Local;
use git2::Repository;
use regex::Regex;
use semver::Version;

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Commit<'a> {
    pub msg: &'a str,
}

pub enum VersionLevel {
    MAJOR,
    MINOR,
    PATCH,
}

pub fn today_iso8601() -> String {
    Local::now().format("%Y-%m-%d").to_string()
}

pub fn enabled_version_flag_count(major: bool, minor: bool, patch: bool) -> i32 {
    let mut count = 0;
    if major { count += 1; }
    if minor { count += 1; }
    if patch { count += 1; }
    count
}

pub fn get_version_level(major: bool, minor: bool, patch: bool) -> Result<VersionLevel, Error> {
    if enabled_version_flag_count(major, minor, patch) != 1 {
        return Err(anyhow!("Too many version flags enabled"));
    }

    if major { return Ok(VersionLevel::MAJOR) }
    if minor { return Ok(VersionLevel::MINOR) }
    Ok(VersionLevel::PATCH)
}

pub fn get_new_version(last_version_raw: &str, level: VersionLevel) -> String {
    let mut last_version: Version = Version::parse(last_version_raw).unwrap();

    match level {
        VersionLevel::MAJOR => {
            last_version.major += 1;
            last_version.minor = 0;
            last_version.patch = 0;
        }
        VersionLevel::MINOR => {
            last_version.minor += 1;
            last_version.patch = 0;
        }
        VersionLevel::PATCH => {
            last_version.patch += 1;
        }
    }

    last_version.to_string()
}

pub fn get_repository() -> Repository {
    Repository::open(".").unwrap()
}

pub fn parse_git_log(stdout: &str) -> impl Iterator<Item=Commit> + '_ {
    let pattern = Regex::new(
        r"(?x)
            ([0-9a-fA-F]+) # commit hash
            (.*)           # The commit message",
    )
        .unwrap();

    stdout
        .lines()
        .filter_map(move |line| pattern.captures(line))
        .map(|cap| Commit {
            msg: cap.get(2).unwrap().as_str().trim(),
        })
}

pub fn parse_commit_message(s: &str) -> String {
    // Neatly format Dependabot entries so that I can easily reorder them later
    if s.starts_with("build(deps): bump ") {
        let s_parts: Vec<_> = s.split(' ').collect();
        let dep_name = s_parts[2];
        let dep_old_ver = s_parts[4];
        let dep_new_ver = s_parts[6];
        let subsystem = s_parts.last().unwrap();
        return format!("\t- {dep_name} ({dep_old_ver} -> {dep_new_ver}) ({subsystem})");
    }

    format!("- {s}")
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_enabled_version_flag_count() {
        assert_eq!(enabled_version_flag_count(true, true, true), 3);
        assert_eq!(enabled_version_flag_count(true, true, false), 2);
        assert_eq!(enabled_version_flag_count(true, false, false), 1);
        assert_eq!(enabled_version_flag_count(false, false, false), 0);
    }


    #[test]
    fn test_get_new_version() {
        let last_version_str = "3.20.3";
        let new_major_ver = get_new_version(last_version_str, VersionLevel::MAJOR);
        assert_eq!(new_major_ver, "4.0.0");
        let new_minor_ver = get_new_version(last_version_str, VersionLevel::MINOR);
        assert_eq!(new_minor_ver, "3.21.0");
        let new_patch_ver = get_new_version(last_version_str, VersionLevel::PATCH);
        assert_eq!(new_patch_ver, "3.20.4");
    }
}