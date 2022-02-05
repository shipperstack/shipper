# Changelog

The format is based on [Keep a Changelog][keep-a-changelog].

[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/

# [Unreleased]


# [1.13.6] - 2022-02-05

## Changed
- Fixed a bug with the build size display in the admin statistics page


# [1.13.5] - 2022-02-05

## Changed
- Fixed a 500 server error in the admin statistics page


# [1.13.4] - 2022-02-05

This release contains a database migration.

## Changed
- Fixed an incorrect database query searching for unmirrored builds preventing the mirroring of builds
- Fixed an incorrect database query searching for unmirrored builds preventing the manual mirroring of builds through admin commands
- shipper now updates the login timestamps on all authenticated API actions
- Fixed admin page to show all possible variants given by the configuration
- The `deinit_full_user` command now includes disabled devices for removal
- General code cleanup


# [1.13.3] - 2022-02-04

## Changed
- Fixed a bug with the build file handler preventing saving to the database and consequently all uploads


# [1.13.2] - 2022-02-02

This release contains a configuration key change.

## Changed
- Fixed an incorrect configuration option (`ADMINS`)


# [1.13.1] - 2022-02-02

This release contains a database migration.

## Changed
- The `target_versions` field in the MirrorServer model now allows for wildcards
- The `upload_backups` management command is now `mirror_builds`


# [1.13.0] - 2022-02-02

This release contains a database migration.
This release contains a new configuration key.

## Added
- Added configuration key for file name delimiter
- Added `build_date` field to Build model
- Added target versions field to MirrorServer model for targeting build versions during mirroring
- Added configuration key for admin emails

## Changed
- Updated `mirrored_on` description warning for the Build model
- Allow for uploads up to 5 GB
- Ignore SSH exceptions and authentication errors stemming from paramiko when reporting to Sentry
- General code cleanup
- Updated library dependencies


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

This release contains an API change.

## Changed
- Fixed a bug with the codename detection where invalid file names could result in an invalid codename being detected
- The internal statistics command now shows more information to the administrator
- Fixed a bug with the template order being processed incorrectly
- The navbar in the maintainer section has been cleaned up
- Many miscellaneous improvements and fixes
- General code cleanup

## Removed
- The `hasBuilds` field has been removed from the v2 all builds API endpoint since it is redundant (only devices with builds are shown in the endpoint
- The shippy notice in the upload menu has been removed, since we're planning to add chunked upload support to the webUI


# [1.6.14] - 2021-06-06

This release contains an API change.

## Changed
- Miscellaneous code cleanup

## Removed
- Some of the unused fields in the v2 all builds API endpoint have been removed


# [1.6.13] - 2021-06-05

This release contains an API change.

## Added
- shipper now has a download favicon

## Changed
- The v2 API for all builds and devices has been expanded in preparation for interfacing with other services and websites
- A bug with the template system has been fixed, and the CSS stylesheet should now function correctly
- Fixed a visual bug on the upload screen: the loading symbol should now display properly for both users with and without screen readers
- Fixed a bug with the API displaying the incorrect connectiono secure schema

## Removed
- The direct upload option through the API has been removed. Old shippy versions that use the direct connection method to upload will no longer function with this release


# [1.6.12] - 2021-05-31

## Changed
- shipper now has a priority field for mirro servers so you can set the priority of the server in the list of mirrors. This field affects the ordering when showing the list of mirrors to the user
- shipper now warns maintaienrs if their account does not have any devices assigned yet
- Fixed a bug with the uploads page not working


# [1.6.11] - 2021-05-26

## Added
- A new all builds APi endpoint has been added

## Changed
- The admin page for MirrorServer now shows more information in the columns and sorts by default
- The main download page no longer puts buttons on separate lines


# [1.6.10] - 2021-05-26

This release contains an API change.

## Changed
- The backup command now queues backups instead of executing them simultaneously
- shipper now displays a mirror page should mirrors exist
- API code has been cleaned

## Removed
- Removed internal API


# [1.6.9] - 2021-05-26

## Added
- Added new management command to get the statistics of shipper (`calculate_statistics`)
- Added new mirror server table

## Changed
- shipper now sorts users by active status first
- Fixed incorrect verbose names for models
- shipper now prints uplaod progress while mirroring a build to a mirror server


# [1.6.8] - 2021-05-25

## Changed
- Fixed a race condition when processing an uploaded build


# [1.6.7] - 2021-05-24

## Changed
- The admin panel shows pretty boolean icons for the "processed" column
- Fixed SHA256 field emptiness detection


# [1.6.6] - 2021-05-24

## Added
- Added locks to prevent multiple backup tasks with the same file from running concurrently
- Added a task to periodically finalize incomplete builds

## Changed
- Correctly display a 401 error instead of a 404 error
- Show column in build admin for "processed" builds


# [1.6.5] - 2021-05-24

## Added
- Added command to finalize incomplete builds
- Added Flower for monitoring tasks

## Changed
- shipper tries to prevent tasks from duplicating the workload


# [1.6.4] - 2021-05-24

## Changed
- The `docker-compose` script now uses the version defined in the environment variable `VERSION_TAG`
- Fixed a bug with the build count


# [1.6.3] - 2021-05-24

This release contains a database migration.
This release contains configuration key changes.

## Added
- Added a docker-compose configuration file for developers
- Added Makefile for developers (used for command alias)
- shipper now supports backing up builds to SourceForge in case the downloads server unexpectedly dies.
- Added library dependencies for shipper (Celery and RabbitMQ)

## Changed
- All shipper configuration variables now start with `SHIPPER_`
- Changed base image (Ubuntu 20.04)
- Docker now copies less files into the image, saving space
- The admin panel now shows the backed up field as a column
- The admin panel now sorts users by last login time
- Sign-ups for new users now require an email address
- SHA256 generation now happens in the background, improving the upload experience


# [1.6.2] - 2021-05-19

## Changed
- Fixed a server error when retrieving an invalid device


# [1.6.1] - 2021-05-19

## Changed
- Devices are now sorted on the main page
- Devices are now sorted on the maintainer page
- Upgraded entire site to Bootstrap v5
- Code cleanup and refactoring


# [1.6.0] - 2021-05-19

This release contains API changes.

## Added
- Added a mini-guide on how to get started with shippy
- Added chunked uploads

## Changed
- shipper now reports the server version in the maintainer API
- Changed maintainer API schema. Old versions of shippy are now incompatible with shipper (and vice versa)
- Changed version information display for normal users
- Changed build name display for normal users
- Fixed styling issue on device page
- Lots and lots of code cleanup and general fix-ups

## Removed
- Removed useless build detail page
- Removed useless notice from password change screen


# [1.5.3] - 2021-05-17

## Changed
- shipper now warns users if the device is not maintained
- shipper now supports showing an alert to ask users for donations. If you want to turn this off, set the `DOWNLOADS_PAGE_DONATION_URL` variable to a single `#`, or omit the variable entirely

## Removed
- Removed some unused fields from the database


# [1.5.2] - 2021-05-17

## Changed
- shipper now shows the creation date column for builds.
- Fixed a bug with creation date ordering
- Users can now download from shipper by going to the relevant device codename page


# [1.5.1] - 2021-04-30

## Changed
- shipper now displays more information about builds


# [1.5.0] - 2021-04-30

This release contains a database migration.

## Changed
- shipper now supports two more variants: FOSS and GoApps


# [1.4.4] - 2021-04-30

## Changed
- shipper now displays the correct download URl to API clients


# [1.4.3] - 2021-04-29

## Changed
- Fixed a small bug with incomplete uploads


# [1.4.2] - 2021-04-28

## Changed
- The API has been fixed to properly throw a 404 if no builds exist for a given variant


# [1.4.1] - 2021-04-28

This release contains a database migration.

## Added
- A new API has been added for LOS-style updater apps. It's not 100% up-to-spec but should require minimal tweaks on the app-side

## Changed
- With the upgrade to Django 3.2, the default ID setting has been changed
- General code cleanup


# [1.4.0] - 2021-04-27

This release contains a security vulnerability patch.

## Changed
- Fixed security vulnerability regarding exceptions
- An incorrect import statement was fixed in the API portion of shipper


# [1.3.1] - 2021-04-27

## Changed
- shipper will strictly enforce the build type and reject any unofficial builds
- Fixed server-side error in API by adding a missing check for the GApps variant
- The upload timeout has been increased to 6 minutes in order to prevent failed uploads


# [1.3.0] - 2021-04-01

## Changed
- Disabled an error metric that has nothing to do with shipper


# [1.2.5] - 2021-02-21

## Changed
- Sentry now reports the version of shipper
- Gunicorn now reports Django errors
- General code cleanup


# [1.2.4] - 2021-02-16

This release contains a configuration key change.

## Changed
- Unified production and development Dockerfiles and configurations. This requires a file name edit - please refer to the wiki for more information
- nginx is now directly downloaded and used without building.
- shipper is now built on Docker Hub and pulled on deployment

## Removed
- shippy is no longer included with the main repository


# [1.2.3] - 2021-02-15

## Changed
- Fixed a UI bug shown to clients


# [1.2.2] - 2021-02-15

## Changed
- shipper finally shows you the upload progress


# [1.2.1] - 2021-02-15

## Added
- Added devcie historical builds page

## Changed
- Fixed nginx configuration to allow large files
- General code cleanup


# [1.2.0] - 2021-02-14

## Added
- Created an internal API for directly manipulating devices/user objects
- Added throttling to the REST API
- Added proper column view to the user admin page

## Changed
- Fixed a bug where the `DEBUG` flag would not register
- Corrected the static file directory configuration
- Fixed a database flushing bug in the development environment
- shipper now shows you its own version at the footer of the maintainer page


# [1.1.0] - 2020-11-21

## Added
- New v2 updater API

## Changed
- Now ships on Docker, with nginx, gunicorn, and Postgres!
- Now supports local storage of files!


# [1.0.0] - 2020-10-26

Initial release


[Unreleased]: https://github.com/ericswpark/shipper/compare/1.13.6...HEAD
[1.13.6]: https://github.com/ericswpark/shipper/compare/1.13.5...1.13.6
[1.13.5]: https://github.com/ericswpark/shipper/compare/1.13.4...1.13.5
[1.13.4]: https://github.com/ericswpark/shipper/compare/1.13.3...1.13.4
[1.13.3]: https://github.com/ericswpark/shipper/compare/1.13.2...1.13.3
[1.13.2]: https://github.com/ericswpark/shipper/compare/1.13.1...1.13.2
[1.13.1]: https://github.com/ericswpark/shipper/compare/1.13.0...1.13.1
[1.13.0]: https://github.com/ericswpark/shipper/compare/1.12.0...1.13.0
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
[1.6.15]: https://github.com/ericswpark/shipper/compare/1.6.14...1.6.15
[1.6.14]: https://github.com/ericswpark/shipper/compare/1.6.13...1.6.14
[1.6.13]: https://github.com/ericswpark/shipper/compare/1.6.12...1.6.13
[1.6.12]: https://github.com/ericswpark/shipper/compare/1.6.11...1.6.12
[1.6.11]: https://github.com/ericswpark/shipper/compare/1.6.10...1.6.11
[1.6.10]: https://github.com/ericswpark/shipper/compare/1.6.9...1.6.10
[1.6.9]: https://github.com/ericswpark/shipper/compare/1.6.8...1.6.9
[1.6.8]: https://github.com/ericswpark/shipper/compare/1.6.7...1.6.8
[1.6.7]: https://github.com/ericswpark/shipper/compare/1.6.6...1.6.7
[1.6.6]: https://github.com/ericswpark/shipper/compare/1.6.5...1.6.6
[1.6.5]: https://github.com/ericswpark/shipper/compare/1.6.4...1.6.5
[1.6.4]: https://github.com/ericswpark/shipper/compare/1.6.3...1.6.4
[1.6.3]: https://github.com/ericswpark/shipper/compare/1.6.2...1.6.3
[1.6.2]: https://github.com/ericswpark/shipper/compare/1.6.1...1.6.2
[1.6.1]: https://github.com/ericswpark/shipper/compare/1.6.0...1.6.1
[1.6.0]: https://github.com/ericswpark/shipper/compare/1.5.3...1.6.0
[1.5.3]: https://github.com/ericswpark/shipper/compare/1.5.2...1.5.3
[1.5.2]: https://github.com/ericswpark/shipper/compare/1.5.1...1.5.2
[1.5.1]: https://github.com/ericswpark/shipper/compare/1.5.0...1.5.1
[1.5.0]: https://github.com/ericswpark/shipper/compare/1.4.4...1.5.0
[1.4.4]: https://github.com/ericswpark/shipper/compare/1.4.3...1.4.4
[1.4.3]: https://github.com/ericswpark/shipper/compare/1.4.2...1.4.3
[1.4.2]: https://github.com/ericswpark/shipper/compare/1.4.1...1.4.2
[1.4.1]: https://github.com/ericswpark/shipper/compare/1.4.0...1.4.1
[1.4.0]: https://github.com/ericswpark/shipper/compare/1.3.1...1.4.0
[1.3.1]: https://github.com/ericswpark/shipper/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/ericswpark/shipper/compare/1.2.5...1.3.0
[1.2.5]: https://github.com/ericswpark/shipper/compare/1.2.4...1.2.5
[1.2.4]: https://github.com/ericswpark/shipper/compare/1.2.3...1.2.4
[1.2.3]: https://github.com/ericswpark/shipper/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/ericswpark/shipper/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/ericswpark/shipper/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/ericswpark/shipper/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/ericswpark/shipper/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/ericswpark/shipper/compare/85a2753f7f234052b8bdf28e0dae98e5042fb99d...1.0.0
