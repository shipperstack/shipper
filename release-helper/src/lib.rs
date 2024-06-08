use std::collections::HashMap;
use std::fmt;
use std::fmt::Formatter;
use anyhow::{anyhow, Error};
use chrono::Local;
use git2::Repository;
use regex::Regex;
use semver::Version;

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Commit<'a> {
    pub msg: &'a str,
}

trait CommitTrait {
    fn is_dependency_commit(&self) -> bool;
    fn to_dependency_commit(&self) -> DependencyCommit;
}

impl<'a> CommitTrait for Commit<'a> {
    fn is_dependency_commit(&self) -> bool {
        self.msg.starts_with("build(deps): bump ")
    }

    fn to_dependency_commit(&self) -> DependencyCommit {
        let s_parts: Vec<_> = self.msg.split(' ').collect();

        if s_parts.len() >= 9 {
            let dep_name = s_parts[2];
            let dep_old_ver = s_parts[4];
            let dep_new_ver = s_parts[6];
            let mut dep_subsystem = s_parts[8].to_string();

            if dep_subsystem.len() > 0 && dep_subsystem.chars().nth(0).unwrap() == '/' {
                dep_subsystem.remove(0);
            }

            return DependencyCommit {
                name: dep_name.to_string(),
                old_ver: dep_old_ver.to_string(),
                new_ver: dep_new_ver.to_string(),
                subsystem: dep_subsystem,
            };
        } else {
            panic!("Not enough parts to construct DependencyCommit");
        }
    }
}

impl<'a> fmt::Display for Commit<'a> {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.msg)
    }
}

pub enum VersionLevel {
    MAJOR,
    MINOR,
    PATCH,
}

#[derive(Clone, Debug, PartialEq)]
pub struct DependencyCommit {
    pub name: String,
    pub old_ver: String,
    pub new_ver: String,
    pub subsystem: String
}

impl fmt::Display for DependencyCommit {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "\t- {} ({} -> {})", self.name, self.old_ver, self.new_ver)
    }
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

pub trait RepositoryTrait {
    fn has_unstaged_changes(&self) -> bool;
}

impl RepositoryTrait for Repository {
    fn has_unstaged_changes(&self) -> bool {
        let diffs = self.diff_index_to_workdir(None, None).expect("Failed to get diffs from the repository!");
        let diff_stats = diffs.stats().expect("Failed to get diff stats from the repository!");
        let files_changed = diff_stats.files_changed();

        files_changed != 0
    }
}

pub fn parse_and_organize(stdout: &str) -> Vec<String> {
    let mut normal_commits = Vec::new();
    let mut dependency_commits: HashMap<String, Vec<DependencyCommit>> = HashMap::new();

    for commit in parse_git_log(stdout) {
        if commit.is_dependency_commit() {
            let dep_commit = commit.to_dependency_commit();

            dependency_commits.entry(dep_commit.subsystem.clone()).or_insert(Vec::new()).push(dep_commit);
        } else {
            normal_commits.push(commit);
        }
    }

    let mut commit_msgs = Vec::new();

    for commit in normal_commits {
        commit_msgs.push(format!("- {commit}"))
    }
    
    for subsystem in dependency_commits {
        let subsystem_name = subsystem.0;
        commit_msgs.push(format!("- Updated dependencies ({subsystem_name})"));
        for commit in subsystem.1 {
            commit_msgs.push(commit.to_string());
        }
    }

    commit_msgs
}

fn parse_git_log(stdout: &str) -> impl Iterator<Item=Commit> + '_ {
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