# Changelog

The format is based on [Keep a Changelog][keep-a-changelog].

[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/

## Warning

This file is incomplete. Please refer to the GitHub Releases page for past releases while this changelog file is being updated.


# [Unreleased]


# [1.12.0] - 2022-01-28

This release contains a database migration.
This release contains a security vulnerability patch.

## Changed
- Fixed a bug with the database schema that prevented build uploads that exceeded the size of 2.1 GB
- Updated to Django 3.2.11 to fix a security vulnerability
- Updated library dependencies


# [1.11.2] - 2022-01-09

This release contains security vulnerability patches.

## Changed
- Updated to Django 3.2.10 to fix a security vulnerability
- Updated to Celery 5.2.3 to fix a security vulnerability
- Updated library dependencies


# [1.11.1] - 2021-10-06

## Changed
- Fixed a regression that caused disabled devices or devices with no builds to not show up under the maintainer dashboard


# [1.11.0] - 2021-10-06

This release contains a configuration key change.

## Changed
- The variant configuration key now includes user-friendly names for each variant
- Fixed theming on the build download page
- The "Back to main website" button no longer shows if the related configuration key is left out
- The maintainer page now uses standard checkbox inputs to toggle build enable status
- Fixed a regression introduced in 1.10.2 where the maintainer page would not show all builds
- General code cleanup


# [1.10.3] - 2021-10-06

## Changed
- Fixed API to get latest build by date instead of ID
- Changed date representation to ISO 8601 for easier reading
- Updated build download page template theming


# [1.10.2] - 2021-10-06

## Changed
- Fixed sorting methods to use build date instead of upload date
- Fixed typo in management command
- Fixed docker-compose file not using quotes
- General code cleanup
- Updated library dependencies


# [1.10.1] - 2021-10-05

## Changed
- Fixed a regression introduced in 1.10.0 that caused a 500 server error on the maintainer dashboard
- Redesigned the maintainer dashboard page to match the main downloads page


# [1.10.0] - 2021-10-05

This release contains a new configuration key.

## Added
- The variants can now be specified in the configuration

## Removed
- The option to upload via WebUI was removed completely


# [1.9.16] - 2021-10-05

## Changed
- The upload page logs unexpected errors to the console for easier debugging


# [1.9.15] - 2021-10-03

## Changed
- Rewrote download counter using vanilla JS
- Fixed a bug where the disable buttons on the build list would only work for the first build in the list
- The maintainer page now shows the correct HTTP error response
code of 403 instead of a generic 404 if the maintainer does not
have the necessary permissions to modify the given device
- Made the build upload page resilient against errors and disabled
inputs on upload start
- Changed dirty way of updating the page after the upload has
completed, which means navigation history is preserved and the
reloaded webpage keeps state
- General code cleanup

## Removed
- Removed JQuery dependency on downloads page





[Unreleased]: https://github.com/ericswpark/shipper/compare/1.12.0...HEAD
[1.12.0]: https://github.com/ericswpark/shipper/compare/1.11.2...1.12.0
[1.11.2]: https://github.com/ericswpark/shipper/compare/1.11.1...1.11.2
[1.11.1]: https://github.com/ericswpark/shipper/compare/1.11.0...1.11.1
[1.11.0]: https://github.com/ericswpark/shipper/compare/1.10.3...1.11.0
[1.10.3]: https://github.com/ericswpark/shipper/compare/1.10.2...1.10.3
[1.10.2]: https://github.com/ericswpark/shipper/compare/1.10.1...1.10.2
[1.10.1]: https://github.com/ericswpark/shipper/compare/1.10.0...1.10.1
[1.10.0]: https://github.com/ericswpark/shipper/compare/1.9.16...1.10.0
[1.9.16]: https://github.com/ericswpark/shipper/compare/1.9.15...1.9.16
[1.9.15]: https://github.com/ericswpark/shipper/compare/1.9.14...1.9.15
