mod constants;
use crate::constants::*;

use clap::{Parser, Subcommand};
use std::fs;
use std::io::BufReader;
use std::process::Command;
use std::{io::BufRead, path::Path};
use chrono::Local;
use git2::Repository;

use semver::Version;

use regex::Regex;

const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Parser, Debug)]
#[command(name = "shipper-release")]
#[command(author = "Eric Park <me@ericswpark.com>")]
#[command(version = VERSION)]
#[command(about="Release orchestrator and changelog management program for shipper", long_about = None)]
struct Cli {
    #[arg(short, long)]
    verbose: bool,
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Generates a CHANGELOG entry with the git commit log
    Generate {
        #[arg(long)]
        major: bool,
        #[arg(long)]
        minor: bool,
        #[arg(short, long)]
        patch: bool,
    },
    /// Creates and pushes a new release to GitHub
    Push,
}

fn main() {
    if !check_running_directory() {
        println!(
            "Unable to find repository files. Are you sure you're running \
this program in the shipper repository?"
        );
        return;
    }

    let cli = Cli::parse();

    match &cli.command {
        Commands::Generate {
            major,
            minor,
            patch,
        } => {
            if !major && !minor && !patch {
                println!(
                    "At least one version flag should be specified. Valid \
options are: --major, --minor, --patch"
                );
                return;
            }
            if enabled_version_flag_count(*major, *minor, *patch) > 1 {
                println!("Only one version flag should be specified.");
                return;
            }
            generate(*major, *minor, *patch);
        }
        Commands::Push => {
            push();
        }
    }
}

/// Function to check if shipper-release is running in the correct directory
fn check_running_directory() -> bool {
    if let Err(_) = Repository::open(".") {
        return false;
    };

    for file in [CHANGELOG_FILE_NAME, VERSION_FILE_NAME] {
        if !Path::new(file).exists() {
            return false;
        }
    }

    true
}

fn enabled_version_flag_count(major: bool, minor: bool, patch: bool) -> i32 {
    let mut count = 0;
    if major { count += 1; }
    if minor { count += 1; }
    if patch { count += 1; }
    count
}

fn today_iso8601() -> String {
    Local::now().format("%Y-%m-%d").to_string()
}

fn generate(major: bool, minor: bool, patch: bool) {
    // Get last version
    let last_version: String = get_last_version();

    let git_log_raw: String = get_git_log_raw(&last_version);

    let new_version: String = get_new_version(&last_version, major, minor, patch);

    println!("New version is {}", new_version);

    update_changelog(&git_log_raw, &last_version, &new_version);

    write_version_files(&new_version);

    println!("Done! Modify the changelog items as necessary, add with `git add .`, and run `shipper-release push`.")
}

fn update_changelog(git_log_raw: &str, last_version: &str, new_version: &str) {
    let binding = fs::read_to_string(CHANGELOG_FILE_NAME)
        .expect("Failed to read the changelog file into memory!");
    let old_changelog = binding.split('\n');

    let mut new_changelog: Vec<String> = Vec::new();

    let today_iso8601 = today_iso8601();

    // Loop until unreleased link line
    for line in old_changelog {
        if line.starts_with(&format!("[Unreleased]: {GITHUB_REPOSITORY_URL}/compare/")) {
            new_changelog.push(format!("[Unreleased]: {GITHUB_REPOSITORY_URL}/compare/{new_version}...HEAD"));

            // Push two empty lines for readability
            new_changelog.push(String::from(""));
            new_changelog.push(String::from(""));

            // Create new changelog entry
            new_changelog.push(format!("# [{new_version}] - {today_iso8601}"));

            new_changelog.push(String::from(""));



            // Add all commit entries (to be sorted later)
            for commit in parse_git_log(git_log_raw) {
                new_changelog.push(parse_commit_message(commit.msg));
            }

            new_changelog.push(String::from(""));

            new_changelog.push(format!("[{new_version}]: {GITHUB_REPOSITORY_URL}/compare/{last_version}...{new_version}"));
            continue;
        } else {
            new_changelog.push(line.to_string());
        }
    }

    // Overwrite changelog file
    fs::write(CHANGELOG_FILE_NAME, new_changelog.join("\n"))
        .expect("Failed to write the new changelog contents!");

    println!("Changelog entries added.");
}

fn parse_commit_message(s: &str) -> String {
    // Neatly format Dependabot entries so that I can easily reorder them later
    if s.starts_with("build(deps): bump ") {
        let s_parts: Vec<_> = s.split(' ').collect();
        let dep_name = s_parts[2];
        let dep_old_ver = s_parts[4];
        let dep_new_ver = s_parts[6];
        let subsystem = s_parts.last().unwrap();
        return format!("\t- {dep_name} ({dep_old_ver} -> {dep_new_ver}) ({subsystem})")
    }

    format!("- {s}")
}

fn write_version_files(new_version: &str) {
    fs::write(VERSION_FILE_NAME, new_version).expect("Failed to write the new version text file!");
    fs::write(SERVER_VERSION_FILE_NAME, new_version).expect("Failed to write the new server version text file!");
    fs::write(SHIPPY_VERSION_FILE_NAME, format!("__version__ = \"{new_version}\"")).expect("Failed to write the new shippy version text file!");

    println!("Version text updated.");
}

fn get_new_version(last_version_raw: &str, major: bool, minor: bool, patch: bool) -> String {
    let mut last_version: Version = Version::parse(last_version_raw).unwrap();

    if major {
        last_version.major += 1;
        last_version.minor = 0;
        last_version.patch = 0;
    } else if minor {
        last_version.minor += 1;
        last_version.patch = 0;
    } else if patch {
        last_version.patch += 1;
    } else {
        panic!("This error shouldn't occur -- failed to get new version string!");
    }

    last_version.to_string()
}

fn get_git_log_raw(last_version: &str) -> String {
    // Get git log between last version and HEAD
    let git_log_output = Command::new("git")
        .arg("log")
        .arg("--oneline")
        .arg("--reverse")
        .arg(format!("{last_version}...HEAD"))
        .output()
        .unwrap();

    if !git_log_output.status.success() {
        panic!("Failed to execute git log command!");
    }

    String::from_utf8(git_log_output.stdout).unwrap()
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct Commit<'a> {
    msg: &'a str,
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

fn get_last_version() -> String {
    // We assume that the user has not modified the version.txt file yet
    let file: fs::File = fs::File::open("version.txt").expect("Unable to open version text file!");

    let mut buffer = BufReader::new(file);
    let mut version_line = String::new();
    buffer
        .read_line(&mut version_line)
        .expect("Cannot read line from version string buffer!");

    version_line.trim().to_string()
}

fn push() {
    let version = get_last_version();

    let changes = get_changes(&version);

    Command::new("git")
        .arg("commit")
        .arg("-m")
        .arg(format!("release: {version}\n\n{changes}"))
        .status()
        .expect("Failed to git commit");
    Command::new("git")
        .arg("tag")
        .arg(version)
        .status()
        .expect("Failed to tag last git commit");

    Command::new("git")
        .arg("push")
        .status()
        .expect("Failed to push release to GitHub");
    Command::new("git")
        .arg("push")
        .arg("--tags")
        .status()
        .expect("Failed to push tag to GitHub");
}

fn get_changes(version: &str) -> String {
    let changelog_content =
        fs::read_to_string(CHANGELOG_FILE_NAME).expect("Cannot read the changelog file to memory!");

    println!("Got version: {}", version);

    let start_marker: String = format!("# [{version}] - ");
    let end_marker: String = format!("[{version}]: {GITHUB_REPOSITORY_URL}/compare/");

    let mut extracted_changes: String = String::new();
    let mut is_in_target_version_section: bool = false;

    for line in changelog_content.lines() {
        if line.starts_with(&start_marker) {
            is_in_target_version_section = true;
            continue;
        } else if line.starts_with(&end_marker) {
            break;
        }

        if is_in_target_version_section && !line.starts_with('#') {
            extracted_changes.push_str(line);
            extracted_changes.push('\n');
        }
    }

    extracted_changes
}
