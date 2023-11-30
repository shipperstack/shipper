# Changelog

The format is based on [Keep a Changelog][keep-a-changelog].

[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/

# Unreleased

# [0.0.7] - 2023-11-30

## Changed
- Updated library dependencies
    - rustix (0.38.7 -> 0.38.19)
- Reformat commit messages from Dependabot
- Use chrono instead of time (back again?) due to offset bugs
- General code cleanup

[0.0.7]:

# [0.0.6] - 2023-08-06

## Changed
- Updated Cargo dependencies

[0.0.6]: https://github.com/shipperstack/shipper/commit/d145a90b2cd815fc1587f6051361f4df74779dbc

# [0.0.5] - 2023-08-06

## Changed
- Updates server subproject's version text file

[0.0.5]: https://github.com/shipperstack/shipper/commit/db057287d281794fe196c7968559e0b3815ae928

# [0.0.4] - 2023-08-02

## Changed
- Updates shippy subproject's version text file
- General code cleanup

[0.0.4]: https://github.com/shipperstack/shipper/commit/5e7dad2b1249e143b935520c45fb679cf19bd493

# [0.0.3] - 2023-07-17

## Changed
- Use `time` crate instead of `chrono` to fix security vulnerability
- Clean up code with clippy
- Testing the new release workflow with GitHub Actions

[0.0.3]: https://github.com/shipperstack/shipper-release/compare/0.0.2...0.0.3

# [0.0.2] - 2023-07-05

## Changed

- Fixed a bug where major and minor version increments wouldn't reset the lower version levels
- The `push` subcommand no longer adds the changed files to git before committing
- Fixed the changelog extracter including headers into the commit message

[0.0.2]: https://github.com/shipperstack/shipper-release/compare/0.0.1...0.0.2

# [0.0.1] - 2023-07-04

Initial release

[0.0.1]: https://github.com/shipperstack/shipper-release/compare/0e062087e64e764672d496c792bdbafabd264b3b...0.0.1
