# [shipper-release](https://crates.io/crates/shipper-release)

Rust program for managing releases and generating changelogs for the shipper project

## Usage

On a clean git state (`git status` shows no uncommitted changes and you already have the new commits pulled to your local repository), generate the new changelog and bump the version string with the following command:

```
shipper-release generate [--major|minor|patch]
```

Note that you must use one level only -- you cannot increment two or more semantic version levels at once!

Once the changelog has been generated, edit it and make the necessary formatting changes. Then run `git add .` to stage the changes, but do not commit. Then run:

```
shipper-release push
```

The release script will then make a commit, tag the commit, and push the commit and tag to the remote repository.


## Development installation

Run

```
cargo install --path . --debug
```

inside the repository.

## Installation

Run

```
cargo install --path .
```