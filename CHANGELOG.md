# Changelog

The format is based on [Keep a Changelog][keep-a-changelog].

[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/

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


# [1.9.14] - 2021-10-02

## Changed
- Completely redesigned main downloads page
- Rewrote build upload page for maintainers to vanilla JS
- General code cleanup
- Updated library dependencies

## Removed
- Removed JQuery dependency on build upload page


# [1.9.13] - 2021-09-29

## Changed
- Fixed typo on one fo the templates
- Moved statistics calculation to a staff-only page instead of an internal command for easy access
- Updated library dependencies

## Removed
- Removed JQuery dependency on device management page


# [1.9.12] - 2021-09-21

## Changed
- Disallow sign-ups with the same email address


# [1.9.11] - 2021-09-08

## Changed
- The statistic in the admin panel now sorts by newer date in descending order, correctly
- Lowered transaction rate of Sentry to avoid hitting limits
- Updated library dependencies


# [1.9.10] - 2021-08-05

This release contains new configuration keys.

## Added
- New security settings keys

## Changed
- Fixed a bug with the downloads page where a device with no builds would show up with an empty row
- Static files are now included with shipper for faster loading times instead of being fetched from CDN
- Fixed a bug with uploading builds where the redirect after success would result in a broken page redner
- Updated library dependencies
- General code cleanup


# [1.9.9] - 2021-07-27

## Changed
- Fixed a 500 bug when fetching the latest build for a given device or variant, if the specified device didn't have any builds for the specified variant
- The downloads template now uses the proper link class for the donation alert
- Updated library dependencies


# [1.9.8] - 2021-07-22

## Added
- Added an optional configuration option to allow customization of the donation message shown at the head of the website
- Added API endpoints for general usage outside of shipper

## Changed
- General code cleanup


# [1.9.7] - 2021-07-22

## Changed
- Fixed a critical bug that would cause a 500 server error on the main page of the website
- Fixed a database access bug with the download count increment code
- Fixed a bug in the auto-retry statement of Celery


# [1.9.6] - 2021-07-22

## Added
- Added more build information on the download page

## Changed
- Download latest build buttons are now "dimmed" instead of being in a "hidden" state
- Fixed a bug where download icons would not appear on mirror server entries
- Massive code cleanup!


# [1.9.5] - 2021-07-22

Re-release of 1.9.4


# [1.9.4] - 2021-07-22

Re-release of 1.9.3


# [1.9.3] - 2021-07-21

Re-release of 1.9.2


# [1.9.2] - 2021-07-21

## Added
- Added new Font Awesome icons for the download page

## Changed
- Fixed incorrect "full name" column in admin panel of accounts
- Fixed an exception that could occur when incrementing download statistic counts
- Changed time limit for all Celery tasks to 10 minutes (previously 1 hour) to reduce server load
- shipper now automatically retries the mirror backup task if it times out, using staggering with exponential backoff and after at least 1 hour since the last attempt to account for any potential mirror server problems
- Fixed a possible race condition while updating the SHA256 hash of a build
- Fixed spacing for the download buttons on the main page
- General code cleanup

## Removed
- Removed a useless title attribute on the download page


# [1.9.1] - 2021-07-14

This release contains new configuration keys.

## Added
- Added new password reset via email feature

## Changed
- Changes to the user model is now recorded on the audit log


# [1.9.0] - 2021-07-13

This release requires an in-between update to 1.8.3 if upgrading from 1.8.2 or below.

## Changed
- shipper finally uses a custom user model


# [1.8.3] - 2021-07-13

This release is an in-between release for users running 1.8.2 or below.


# [1.8.2] - 2021-07-11

This release contains an API change.

## Changed
- Fixed a bug where the download count for the past 24 hours API endpoint woudl use the incorrect time range
- Fixed a race condition when incrementing the download counters
- Fixed an incorrect request type being used (shippy 1.5.1 or above is required to interface with this release)
- Fixed a server error bug that would manifest from operating on a field too early, if the field was blank in the request
- Lots of code cleanup and optimizations

## Removed
- Removed the v2 all builds API endpoint due to lack of use
- Removed the v2 updater device API endpoint as it was not being used


# [1.8.1] - 2021-07-10

This release contains an API change.

## Added
- Added download count API endpoints to query download counts for the last 24 hours, last 7 days, and last 31 days

## Changed
- Fixed a display bug in the admin panel where "Statisticss" had an additional 's'
- Disabled web-based view for DRF (Django REST Framework). Responses should now show as plain JSON instead of a web page, and POSTing directly from the browser has now been disabled
- The updater API now uses DRF instead of Django to return responses, for both v1 and v2 endpoints
- The updater API now returns a 400 if the supplied variant name is invalid
- The updater API now returns a more descriptive 404 message
- Reduced throttling rates for anonymous users
- Fixed a bug with nginx passing the incorrect HOST header to shipper
- Fixed a bug with Django generating the redirect URL for the API
- General code cleanup


# [1.8.0] - 2021-07-10

This release contains a database migration.
This release contains an API change.

## Added
- A database model to track daily downloads has been added

## Changed
- The admin page for builds nwo shows the download count as a column
- All API endpoints have been moved to the "API" app and refactored (requires shippy 1.5.0 and above to interface with this release)
- General code cleanup
- Updated library dependencies


# [1.7.4] - 2021-07-04

## Changed
- Fixed a bug with the audit log filling up with download counter changes


# [1.7.3] - 2021-07-04

This release contains a database migration.

## Added
- Added a new alert banner for users if debug mode is enabled to make sure users do not accidentally use testing environments
- Added download counter to build model
- Added an API endpoint to increase the download counter

## Changed
- Fixed a counting bug with statistics calculation for administrators
- The API throttling rates have been adjusted to reduce server load
- General code cleanup


# [1.7.2] - 2021-07-03

This release contains security vulnerability patches.

## Added
- Added an "audit log" to log changes across all models

## Changed
- Updated Django to 3.2.5 to patch security vulnerabilities
- Updated library dependencies


# [1.7.1] - 2021-07-01

## Added
- Added management command to de-initialize a "full" user account
- Added enabled field as a column and filter option in the admin panel for build objects

## Changed
- Fixed a bug with setting the enabled field of builds to true for new uploads


# [1.7.0] - 2021-06-29

This release contains a database migration.

## Added
- Added a command to initialize a "full" user - i.e. user with access to all devices. This is useful if you want to create a build bot user that can upload to all devices. Note that this user **must** already exist within the system!
- Build objects can now be "enabled" and "disabled." When build objects are disabled, they are hidden from users and the API endpoints
- Added a maintainer endpoint to enable/disable builds on upload

## Changed
- shipper now signs out the user if the password has been changed
- Updated token invalidation message on the password change screen
- The admin panel now allows filtering of devices by status
- The admin panel now allows filtering of mirror servers by enabled/downloadable status
- The build ID is now exposed to maintainers on a successful upload
- Updated library dependencies

## Removed
- Removed the redirect to dashboard button on the sign-up screen


# [1.6.16] - 2021-06-18

## Added
- Added an endpoint for shippy to check token validity

## Changed
- shipper now invalidates the authentication token if the password has been changed
- Fixed a bug where the admin password change template would get overridden with the custom password change template


# [1.6.15] - 2021-06-18

(WIP)



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
[1.9.14]: https://github.com/ericswpark/shipper/compare/1.9.13...1.9.14
[1.9.13]: https://github.com/ericswpark/shipper/compare/1.9.12...1.9.13
[1.9.12]: https://github.com/ericswpark/shipper/compare/1.9.11...1.9.12
[1.9.11]: https://github.com/ericswpark/shipper/compare/1.9.10...1.9.11
[1.9.10]: https://github.com/ericswpark/shipper/compare/1.9.9...1.9.10
[1.9.9]: https://github.com/ericswpark/shipper/compare/1.9.8...1.9.9
[1.9.8]: https://github.com/ericswpark/shipper/compare/1.9.7...1.9.8
[1.9.7]: https://github.com/ericswpark/shipper/compare/1.9.6...1.9.7
[1.9.6]: https://github.com/ericswpark/shipper/compare/1.9.5...1.9.6
[1.9.5]: https://github.com/ericswpark/shipper/compare/1.9.4...1.9.5
[1.9.4]: https://github.com/ericswpark/shipper/compare/1.9.3...1.9.4
[1.9.3]: https://github.com/ericswpark/shipper/compare/1.9.2...1.9.3
[1.9.2]: https://github.com/ericswpark/shipper/compare/1.9.1...1.9.2
[1.9.1]: https://github.com/ericswpark/shipper/compare/1.9.0...1.9.1
[1.9.0]: https://github.com/ericswpark/shipper/compare/1.8.3...1.9.0
[1.8.3]: https://github.com/ericswpark/shipper/compare/1.8.2...1.8.3
[1.8.2]: https://github.com/ericswpark/shipper/compare/1.8.1...1.8.2
[1.8.1]: https://github.com/ericswpark/shipper/compare/1.8.0...1.8.1
[1.8.0]: https://github.com/ericswpark/shipper/compare/1.7.4...1.8.0
[1.7.4]: https://github.com/ericswpark/shipper/compare/1.7.3...1.7.4
[1.7.3]: https://github.com/ericswpark/shipper/compare/1.7.2...1.7.3
[1.7.2]: https://github.com/ericswpark/shipper/compare/1.7.1...1.7.2
[1.7.1]: https://github.com/ericswpark/shipper/compare/1.7.0...1.7.1
[1.7.0]: https://github.com/ericswpark/shipper/compare/1.6.16...1.7.0
[1.6.16]: https://github.com/ericswpark/shipper/compare/1.6.15...1.6.16

