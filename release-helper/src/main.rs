mod constants;

use crate::constants::*;

use shipper_release::*;

use clap::{Parser, Subcommand};
use std::fs;
use std::io::BufReader;
use std::process::{Command, exit};
use std::{io::BufRead, path::Path};
use git2::{Error, ObjectType, PushOptions, RemoteCallbacks, Repository, Signature};

const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Parser, Debug)]
#[command(name = "shipper-release")]
#[command(author = "Eric Park <me@ericswpark.com>")]
#[command(version = VERSION)]
#[command(
    about = "Release orchestrator and changelog management program for shipper", long_about = None
)]
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

            generate(get_version_level(*major, *minor, *patch).unwrap());
        }
        Commands::Push => {
            push().unwrap_or_else(|error| {
                println!("Failed to create a commit and push to remote: {error}");
                exit(1);
            });
        }
    }
}

/// Function to check if shipper-release is running in the correct directory
fn check_running_directory() -> bool {
    if Repository::open(".").is_err() {
        return false;
    };

    for file in [CHANGELOG_FILE_NAME, VERSION_FILE_NAME] {
        if !Path::new(file).exists() {
            return false;
        }
    }

    true
}

fn generate(version_level: VersionLevel) {
    // Get last version
    let last_version: String = get_last_version();

    let git_log_raw: String = get_git_log_raw(&last_version);

    let new_version: String = get_new_version(&last_version, version_level);

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

            // Add all organized commit entries
            let organized_commit_messages = parse_and_organize(git_log_raw);
            new_changelog.extend(organized_commit_messages);

            new_changelog.push(String::from(""));

            new_changelog.push(format!("[{new_version}]: {GITHUB_REPOSITORY_URL}/compare/{last_version}...{new_version}"));
            continue;
        } else {
            // Write previous releases
            new_changelog.push(line.to_string());
        }
    }

    // Overwrite changelog file
    fs::write(CHANGELOG_FILE_NAME, new_changelog.join("\n"))
        .expect("Failed to write the new changelog contents!");

    println!("Changelog entries added.");
}

fn write_version_files(new_version: &str) {
    fs::write(VERSION_FILE_NAME, new_version).expect("Failed to write the new version text file!");
    fs::write(SERVER_VERSION_FILE_NAME, new_version).expect("Failed to write the new server version text file!");
    fs::write(SHIPPY_VERSION_FILE_NAME, format!("__version__ = \"{new_version}\"")).expect("Failed to write the new shippy version text file!");

    println!("Version text updated.");
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

fn push() -> Result<(), Error> {
    let version = get_last_version();

    let changes = get_changes(&version);

    let repo = get_repository();

    if repo.has_unstaged_changes() {
        return Err(Error::from_str("Repository has unstaged changes!"));
    }

    let mut index = repo.index()?;
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;

    let head = repo.head()?;
    let parent_commit = head.peel_to_commit()?;

    let config = repo.config()?;
    let name = config.get_string("user.name")?;
    let email = config.get_string("user.email")?;
    let signature = Signature::now(&name, &email)?;

    let commit_msg = format!("release: {version}\n\n{changes}");

    let commit_oid = repo.commit(
        Some("HEAD"),
        &signature,
        &signature,
        &commit_msg,
        &tree,
        &[&parent_commit],
    )?;
    println!("New commit ID: {commit_oid}");

    let commit_obj = repo.find_object(commit_oid, Some(ObjectType::Commit))?;
    repo.tag_lightweight(&version, &commit_obj, false)?;
    println!("Created tag {version} for commit ID {commit_oid}");

    let head_ref = repo.head()?.resolve()?;
    let branch_name = head_ref.name().ok_or_else(|| {
        Error::from_str("Failed to get branch name")
    })?;
    let branch_shortname = head_ref.shorthand().ok_or_else(|| {
        Error::from_str("Failed to get branch shortname")
    })?;
    let upstream_remote = repo.branch_upstream_remote(branch_name)?;
    let remote_name = upstream_remote.as_str().ok_or_else(|| {
        Error::from_str("Failed to get remote name")
    })?;
    let mut remote = repo.find_remote(remote_name)?;

    let mut callbacks = RemoteCallbacks::new();
    callbacks.credentials(|_url, _username_from_url, _allowed_types| {
        git2::Cred::ssh_key_from_agent("git")
    });

    let mut push_options = PushOptions::new();
    push_options.remote_callbacks(callbacks);

    print!("Pushing branch {branch_shortname} to remote {remote_name}... ");
    remote.push(&[&branch_name], Some(&mut push_options))?;
    println!("Done");

    print!("Pushing tag {version} to remote {remote_name}... ");
    remote.push(&[&format!("refs/tags/{}", &version)], Some(&mut push_options))?;
    println!("Done");

    Ok(())
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
