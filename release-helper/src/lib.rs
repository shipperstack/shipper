use anyhow::{anyhow, Error};
use chrono::Local;
use git2::Repository;
use regex::Regex;
use semver::Version;
use std::cmp::{max, min};
use std::collections::HashMap;
use std::fmt;
use std::fmt::Formatter;

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Commit<'a> {
    pub msg: &'a str,
}

trait CommitTrait {
    fn is_dependency_commit(&self) -> bool;
    fn to_dependency_commit(&self) -> Result<DependencyCommit, Error>;
}

const DEP_COMMIT_PART_COUNT: usize = 9;

impl<'a> CommitTrait for Commit<'a> {
    fn is_dependency_commit(&self) -> bool {
        (self.msg.starts_with("build(deps): bump ")
            || self.msg.starts_with("build(deps-dev): bump "))
            && self.msg.split(' ').count() >= DEP_COMMIT_PART_COUNT
    }

    fn to_dependency_commit(&self) -> Result<DependencyCommit, Error> {
        let s_parts: Vec<_> = self.msg.split(' ').collect();

        if s_parts.len() >= DEP_COMMIT_PART_COUNT {
            let dep_name = s_parts[2];
            let dep_old_ver = s_parts[4];
            let dep_new_ver = s_parts[6];
            let mut dep_subsystem = s_parts[8].to_string();

            if !dep_subsystem.is_empty() && dep_subsystem.chars().nth(0).unwrap() == '/' {
                dep_subsystem.remove(0);
            }

            Ok(DependencyCommit {
                name: dep_name.to_string(),
                old_ver: Version::parse(dep_old_ver).unwrap(),
                new_ver: Version::parse(dep_new_ver).unwrap(),
                subsystem: dep_subsystem,
            })
        } else {
            Err(anyhow!("Not enough parts to construct DependencyCommit"))
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
    pub old_ver: Version,
    pub new_ver: Version,
    pub subsystem: String,
}

impl fmt::Display for DependencyCommit {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "\t- {} ({} -> {})",
            self.name, self.old_ver, self.new_ver
        )
    }
}

pub fn today_iso8601() -> String {
    Local::now().format("%Y-%m-%d").to_string()
}

pub fn enabled_version_flag_count(major: bool, minor: bool, patch: bool) -> i32 {
    [major, minor, patch].into_iter().filter(|b| *b).count() as i32
}

pub fn get_version_level(major: bool, minor: bool, patch: bool) -> Result<VersionLevel, Error> {
    if enabled_version_flag_count(major, minor, patch) != 1 {
        return Err(anyhow!("Too many version flags enabled"));
    }

    if major {
        return Ok(VersionLevel::MAJOR);
    }
    if minor {
        return Ok(VersionLevel::MINOR);
    }
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
        let diffs = self
            .diff_index_to_workdir(None, None)
            .expect("Failed to get diffs from the repository!");
        let diff_stats = diffs
            .stats()
            .expect("Failed to get diff stats from the repository!");
        let files_changed = diff_stats.files_changed();

        files_changed != 0
    }
}

pub fn parse_and_organize(stdout: &str) -> Vec<String> {
    let parsed_log: Vec<Commit> = parse_git_log(stdout).collect();
    let (normal_commits, dependency_commits) = filter_commits(&parsed_log);

    let mut commit_messages = Vec::new();

    for commit in normal_commits {
        commit_messages.push(format!("- {commit}"))
    }

    for subsystem in dependency_commits {
        let subsystem_name = subsystem.0;
        commit_messages.push(format!("- Updated dependencies ({subsystem_name})"));
        for commit in subsystem.1 {
            commit_messages.push(commit.to_string());
        }
    }

    commit_messages
}

fn filter_commits<'a>(
    parsed_log: &'a Vec<Commit<'a>>,
) -> (Vec<Commit<'a>>, HashMap<String, Vec<DependencyCommit>>) {
    let mut normal_commits: Vec<Commit> = Vec::new();
    let mut dependency_commits: HashMap<String, Vec<DependencyCommit>> = HashMap::new();

    for commit in parsed_log {
        if commit.is_dependency_commit() {
            let dep_commit = commit
                .to_dependency_commit()
                .expect("Dependency commit coercion error");

            if dependency_commits.contains_key(&dep_commit.subsystem) {
                let mut found_existing_commit = false;

                for prev_dep_commit in dependency_commits.get_mut(&dep_commit.subsystem).unwrap() {
                    if prev_dep_commit.name == dep_commit.name {
                        prev_dep_commit.old_ver =
                            min(prev_dep_commit.old_ver.clone(), dep_commit.old_ver.clone());
                        prev_dep_commit.new_ver =
                            max(prev_dep_commit.new_ver.clone(), dep_commit.new_ver.clone());
                        found_existing_commit = true;
                        break;
                    }
                }

                if !found_existing_commit {
                    dependency_commits.get_mut(&dep_commit.subsystem).unwrap().push(dep_commit);
                }
            } else {
                dependency_commits.insert(dep_commit.subsystem.to_string(), vec![dep_commit]);
            }
        } else {
            normal_commits.push(*commit);
        }
    }

    (normal_commits, dependency_commits)
}

fn parse_git_log(stdout: &str) -> impl Iterator<Item = Commit> + '_ {
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

    #[test]
    fn test_filter_commits() {
        let parsed_commits = vec![
            Commit {
                msg: "fix: did some fixing stuff",
            },
            Commit {
                msg: "build(deps): bump semver from 1.0.0 to 1.1.0 in /server",
            },
            Commit {
                msg: "build(deps): bump semver from 1.1.0 to 1.1.1 in /server",
            },
            Commit {
                msg: "build(deps): bump orion from 2.0.0 to 3.2.2 in /shippy",
            },
            Commit {
                msg: "build(deps): bump astro from 1.0.0 to 1.1.1 in /server",
            },
        ];

        let (normal_commits, dependency_commits) = filter_commits(&parsed_commits);

        assert_eq!(normal_commits.len(), 1);
        assert_eq!(dependency_commits.get("server").unwrap().len(), 2);
        assert_eq!(dependency_commits.get("shippy").unwrap().len(), 1);
        assert_eq!(normal_commits[0].msg,  parsed_commits[0].msg);
        assert_eq!(
            dependency_commits
                .get("server")
                .unwrap()
                .iter()
                .filter(|&x| x.name == "semver")
                .collect::<Vec<&DependencyCommit>>()[0]
                .old_ver,
            Version::parse("1.0.0").unwrap()
        );
        assert_eq!(
            dependency_commits
                .get("server")
                .unwrap()
                .iter()
                .filter(|&x| x.name == "semver")
                .collect::<Vec<&DependencyCommit>>()[0]
                .new_ver,
            Version::parse("1.1.1").unwrap()
        );

        assert_eq!(
            dependency_commits
                .get("shippy")
                .unwrap()
                .iter()
                .filter(|&x| x.name == "orion")
                .collect::<Vec<&DependencyCommit>>()[0]
                .old_ver,
            Version::parse("2.0.0").unwrap()
        );
        assert_eq!(
            dependency_commits
                .get("shippy")
                .unwrap()
                .iter()
                .filter(|&x| x.name == "orion")
                .collect::<Vec<&DependencyCommit>>()[0]
                .new_ver,
            Version::parse("3.2.2").unwrap()
        );
    }
}
