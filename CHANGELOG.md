# Changelog

The format is based on [Keep a Changelog][keep-a-changelog].

[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/

# [Unreleased]

[Unreleased]: https://github.com/shipperstack/shipper/compare/2.38.0...HEAD

# [2.38.0] - 2024-05-27

This release contains a database migration.

## Added

- Added a notes field to the Device model

## Changed

- Fixed the server showing the "last updated" text on the device page when no builds are present
- Fixed the `x86_type` field preventing saving of non-x86 devices
- Fixed the release helper script panic-quitting if any errors are encountered during pushing

[2.38.0]: https://github.com/shipperstack/shipper/compare/2.37.9...2.38.0

# [2.37.9] - 2024-05-27

## Changed

- Updated dependencies (shippy)
  - sentry-sdk (2.2.1 -> 2.3.1)
- Updated dependencies (server)
  - sentry-sdk (2.2.1 -> 2.3.1)
- The release helper script now uses the git2 library for robustness
- The release helper script will now no longer push if unstaged changes exist in the working directory
- Updated dependencies (release-helper)
  - chrono (0.4.31 -> 0.4.38)
  - semver (1.0.18 -> 1.0.23)
  - regex (1.9.3 -> 1.10.4)
  - clap (4.3.19 -> 4.5.4) (/release-helper)
- General code cleanup

## Removed

- Removed deprecated `USE_L10N` Django settings key

[2.37.9]: https://github.com/shipperstack/shipper/compare/2.37.8...2.37.9

# [2.37.8] - 2024-05-23

## Changed

- shippy now prints 5xx error codes returned from the server

[2.37.8]: https://github.com/shipperstack/shipper/compare/2.37.7...2.37.8

# [2.37.7] - 2024-05-23

## Changed

- Fixed server generating an error if the build was deleted before mirroring auto-retry occurred
- Updated dependencies (shippy)
  - requests (2.31.0 -> 2.32.2)
  - setuptools (69.5.1 -> 70.0.0)
  - sentry-sdk (2.2.0 -> 2.2.1)
- Updated dependencies (server)
  - requests (2.31.0 -> 2.32.2)
  - sentry-sdk (2.2.0 -> 2.2.1)

[2.37.7]: https://github.com/shipperstack/shipper/compare/2.37.6...2.37.7

# [2.37.6] - 2024-05-17

## Changed

- Updated dependencies (shippy)
  - sentry-sdk (2.1.1 -> 2.2.0)
- Updated dependencies (server)
  - sentry-sdk (2.1.1 -> 2.2.0)
- Fixed server to ignore ImproperlyConfigured exceptions when reporting to Sentry

[2.37.6]: https://github.com/shipperstack/shipper/compare/2.37.5...2.37.6

# [2.37.5] - 2024-05-17

## Changed

- Fixed server Docker image build failing due to pulled dependency versions

[2.37.5]: https://github.com/shipperstack/shipper/compare/2.37.4...2.37.5

# [2.37.4] - 2024-05-17

## Changed

- Fixed the management command trying to queue up mirror jobs for archived builds
- Increased the Celery tasks time limit to one hour
- Fixed the server not checking if the configuration keys are empty (invalid)
- Fixed shippy crashing if the server is temporarily unavailable
- General code cleanup

[2.37.4]: https://github.com/shipperstack/shipper/compare/2.37.3...2.37.4

# [2.37.3] - 2024-05-13

## Added

- Added a setting to the server to globally control mirroring of builds

## Changed

- Fixed the server uploading truncated builds to mirror servers

[2.37.3]: https://github.com/shipperstack/shipper/compare/2.37.2...2.37.3

# [2.37.2] - 2024-05-12

## Changed

- Fixed the server crashing if the SSH key does not exist
- Fixed the server erroring out during the connection to the mirror server
- Fixed the server crashing if the base upload path does not exist on the mirror server
- Fixed shippy not supplying the authentication token when checking for duplicate builds during validation

[2.37.2]: https://github.com/shipperstack/shipper/compare/2.37.1...2.37.2

# [2.37.1] - 2024-05-12

## Changed

- Fixed the build model looking up the mirror server causing crashes

[2.37.1]: https://github.com/shipperstack/shipper/compare/2.37.0...2.37.1

# [2.37.0] - 2024-05-11

## Added

- Added prechecks on shipper and shippy to check build duplicity before uploading

## Changed

- Fixed a bug where the token check API endpoint was caching the results
- Fixed a bug that was causing date conversion test failures on Windows
- Updated dependencies (shippy)
  - sentry-sdk (2.0.1 -> 2.1.1)
- Updated dependencies (server)
  - django (5.0.4 -> 5.0.6)
  - sentry-sdk (2.0.1 -> 2.1.1)
- General code cleanup

[2.37.0]: https://github.com/shipperstack/shipper/compare/2.36.8...2.37.0

# [2.36.8] - 2024-05-06

## Changed

- Fixed shippy not printing why upload starting failed

[2.36.8]: https://github.com/shipperstack/shipper/compare/2.36.7...2.36.8

# [2.36.7] - 2024-05-06

## Changed

- Fixed shippy blocking login with the console status indicator
- Fixed shippy recommending upgrade commands without considering installation method

[2.36.7]: https://github.com/shipperstack/shipper/compare/2.36.6...2.36.7

# [2.36.6] - 2024-05-02

## Changed

- Fixed mirror server URLs not prepending the device codename as the base upload path

[2.36.6]: https://github.com/shipperstack/shipper/compare/2.36.5...2.36.6

# [2.36.5] - 2024-05-02

## Changed

- Updated dependencies (server)
  - @babel/core (7.24.4 -> 7.24.5)
  - @babel/preset-env (7.24.4 -> 7.24.5)
- Fixed broken mirror URLs on the download build pages
- Fixed broken mirror URLs in the API relying on null build files

[2.36.5]: https://github.com/shipperstack/shipper/compare/2.36.4...2.36.5

# [2.36.4] - 2024-04-29

## Changed

- Fixed copying over requirements files

[2.36.4]: https://github.com/shipperstack/shipper/compare/2.36.3...2.36.4

# [2.36.3] - 2024-04-29

## Changed

- Fixed copying over requirements files

[2.36.3]: https://github.com/shipperstack/shipper/compare/2.36.2...2.36.3

# [2.36.2] - 2024-04-29

## Changed

- Fixed pip not installing dependencies due to system management of packages

[2.36.2]: https://github.com/shipperstack/shipper/compare/2.36.1...2.36.2

# [2.36.1] - 2024-04-29

## Changed

- Fixed incorrect PostgreSQL15 client version in Alpine 3.19 crashing build process

[2.36.1]: https://github.com/shipperstack/shipper/compare/2.36.0...2.36.1

# [2.36.0] - 2024-04-29

## Changed

- Updated base Docker image to Alpine 3.19
- Improved build times and caching behavior
- Updated dependencies (server)
  - django-ipware (6.0.5 -> 7.0.1)
  - sentry-sdk (1.45.0 -> 2.0.1)
  - react (18.2.0 -> 18.3.1)
  - react-dom (18.2.0 -> 18.3.1)
- Updated dependencies (shippy)
  - sentry-sdk (1.45.0 -> 2.0.1)

[2.36.0]: https://github.com/shipperstack/shipper/compare/2.35.0...2.36.0

# [2.35.0] - 2024-04-19

This release contains a security vulnerability patch.

## Changed

- Updated dependencies (shippy)
  - setuptools (69.4.0 -> 69.5.1)
- Updated dependencies (server)
  - fuse.js (6.6.2 -> 7.0.0)
  - gunicorn (21.2.0 -> 22.0.0)!
  - celery (5.3.6 -> 5.4.0)

[2.35.0]: https://github.com/shipperstack/shipper/compare/2.34.0...2.35.0

# [2.34.0] - 2024-04-12

This release contains a database migration.

Warning: the database migration may take a long time due to the audit log package being updated.

## Changed

- Restored console logging to default state on the server
- Updated dependencies (server)
  - sentry-sdk (1.44.1 -> 1.45.0)
  - django-ipware (6.0.4 -> 6.0.5)
  - django-auditlog (2.3.0 -> 3.0.0)!
- Updated dependencies (shippy)
  - sentry-sdk (1.44.1 -> 1.45.0)
  - setuptools (69.2.0 -> 69.4.0)

[2.34.0]: https://github.com/shipperstack/shipper/compare/2.33.6...2.34.0

# [2.33.6] - 2024-04-06

## Changed

- Reverted debug code that managed to sneak in during the release process

[2.33.6]: https://github.com/shipperstack/shipper/compare/2.33.5...2.33.6

# [2.33.5] - 2024-04-06

## Changed

- Fixed logging filter not working properly

[2.33.5]: https://github.com/shipperstack/shipper/compare/2.33.4...2.33.5

# [2.33.4] - 2024-04-06

## Changed

- Fixed filtering out 503 errors

[2.33.4]: https://github.com/shipperstack/shipper/compare/2.33.3...2.33.4

# [2.33.3] - 2024-04-06

## Changed

- Fixed server sending emails about 503 errors when download is unavailable

[2.33.3]: https://github.com/shipperstack/shipper/compare/2.33.2...2.33.3

# [2.33.2] - 2024-04-05

This release contains a database migration.

## Changed

- Updated dependencies (server)
  - django (5.0.3 -> 5.0.4)
  - sentry-sdk (1.44.0 -> 1.44.1)
- Updated dependencies (shippy)
  - sentry-sdk (1.44.0 -> 1.44.1)
- fix(server): drop unique requirement from build file
- refactor(server): move main server avail check to models
- fix(server): downloads: return 503 if zip file is offloaded

[2.33.2]: https://github.com/shipperstack/shipper/compare/2.33.1...2.33.2

# [2.33.1] - 2024-04-02

## Changed

- Fixed checking the build file existence in the management command

[2.33.1]: https://github.com/shipperstack/shipper/compare/2.33.0...2.33.1

# [2.33.0] - 2024-04-02

This release contains a database migration.

## Added

- Added command to unset missing build files

## Changed

- Updated library dependencies (shippy)
  - sentry-sdk (1.42.0 -> 1.44.0)
- Updated library dependencies (server)
  - djangorestframework (3.14.0 -> 3.15.0)
  - sentry-sdk (1.42.0 -> 1.44.0)
  - djangorestframework (3.15.0 -> 3.15.1)
- shipper now loads environment variables from a dotfile if it is available
- Build files can now be unset for build offloading

[2.33.0]: https://github.com/shipperstack/shipper/compare/2.32.0...2.33.0

# [2.32.0] - 2024-03-18

## Changed

- Updated library dependencies (shippy)
  - setuptools (69.0.3 -> 69.2.0)
  - sentry-sdk (1.40.3 -> 1.42.0)
  - rich (13.7.0 -> 13.7.1)
- Updated library dependencies (server)
  - django (4.2.10 -> 5.0.3)
  - sentry-sdk (1.40.3 -> 1.42.0)
  - crispy-bootstrap5 (2023.10 -> 2024.2)
  - django-celery-beat (2.5.0 -> 2.6.0)

[2.32.0]: https://github.com/shipperstack/shipper/compare/2.31.0...2.32.0

# [2.31.0] - 2024-02-09

This release contains a security vulnerability patch.

## Added

- Added visible field to Device model to control device visibility on main downloads page

## Changed

- Fixed the Docker updater script crashing if the version is not published yet on GitHub Packages registry
- Updated library dependencies (server)
  - django-cleanup (8.0.0 -> 8.1.0)
  - sentry-sdk (1.39.2 -> 1.40.3)
  - django (4.2.7 -> 4.2.10)
  - django-ipware (6.0.3 -> 6.0.4) (/server)
- Updated library dependencies (shippy)
  - sentry-sdk (1.39.2 -> 1.40.3) (/shippy)

[2.31.0]: https://github.com/shipperstack/shipper/compare/2.30.2...2.31.0

# [2.30.2] - 2024-01-28

- Fixed shippy not logging upload exceptions

[2.30.2]: https://github.com/shipperstack/shipper/compare/2.30.1...2.30.2

# [2.30.1] - 2024-01-27

## Added

- Added debug configuration option for shippy

[2.30.1]: https://github.com/shipperstack/shipper/compare/2.30.0...2.30.1

# [2.30.0] - 2024-01-27

## Changed

- Fixed tests not working properly for the server component
- Fixed exception details getting lost for shippy
- Updated library dependencies (shippy)
  - setuptools (69.0.2 -> 69.0.3)
  - sentry-sdk (1.39.1 -> 1.39.2)
- Updated library dependencies (server)
  - django-dbbackup (4.0.2 -> 4.1.0)
  - sentry-sdk (1.39.1 -> 1.39.2)
- General code cleanup

## Removed

- Removed unnecessary debug output for shippy

[2.30.0]: https://github.com/shipperstack/shipper/compare/2.29.1...2.30.0

# [2.29.1] - 2023-12-25

## Changed

- Fixed the server API not returning the full download URL

[2.29.1]: https://github.com/shipperstack/shipper/compare/2.29.0...2.29.1

# [2.29.0] - 2023-12-25

Merry Christmas!

## Changed

- Fixed the server sending the incorrect download URL in API responses
- Updated library dependencies (server)
  - sentry-sdk (1.39.0 -> 1.39.1)
  - django-ipware (6.0.2 -> 6.0.3)
  - thumbhash-python (1.0.0 -> 1.0.1) (/server)
  - paramiko (3.3.1 -> 3.4.0) (/server)
- Updated library dependencies (shippy)
  - sentry-sdk (1.39.0 -> 1.39.1)

[2.29.0]: https://github.com/shipperstack/shipper/compare/2.28.8...2.29.0

# [2.28.8] - 2023-12-13

## Changed

- Fixed server crashing on fetching file modification time

[2.28.8]: https://github.com/shipperstack/shipper/compare/2.28.7...2.28.8

# [2.28.7] - 2023-12-13

## Changed

- Fixed server corrupting download names by returning correct headers

[2.28.7]: https://github.com/shipperstack/shipper/compare/2.28.6...2.28.7

# [2.28.6] - 2023-12-13

## Changed

- Fixed server mangling the content type for build downloads
- Fixed server download speed setting

[2.28.6]: https://github.com/shipperstack/shipper/compare/2.28.5...2.28.6

# [2.28.5] - 2023-12-13

## Changed

- Fixed server improperly adding a duplicated codename to the build download redirect

[2.28.5]: https://github.com/shipperstack/shipper/compare/2.28.4...2.28.5

# [2.28.4] - 2023-12-13

## Changed

- Fixed server passing wrong file name to nginx

[2.28.4]: https://github.com/shipperstack/shipper/compare/2.28.3...2.28.4

# [2.28.3] - 2023-12-13

## Changed

- Fixed the server using the incorrect pattern matching for the file name

[2.28.3]: https://github.com/shipperstack/shipper/compare/2.28.2...2.28.3

# [2.28.2] - 2023-12-13

## Changed

- Fixed reverse URL not working in production

[2.28.2]: https://github.com/shipperstack/shipper/compare/2.28.1...2.28.2

# [2.28.1] - 2023-12-13

## Changed

- Fix the download check view not being used

[2.28.1]: https://github.com/shipperstack/shipper/compare/2.28.0...2.28.1

# [2.28.0] - 2023-12-13

## Changed

- Fixed the download endpoint not working properly
- Updated library dependencies (server)
  - sentry-sdk (1.38.0 -> 1.39.0)
- Updated library dependencies (shippy)
  - sentry-sdk (1.38.0 -> 1.39.0)

## Removed

- Removed v1 system API endpoint from the server

[2.28.0]: https://github.com/shipperstack/shipper/compare/2.27.0...2.28.0

# [2.27.0] - 2023-12-12

## Changed

- shippy now uses the v2 system endpoint to fetch details about the server
- shippy now requires the server to be at least version 2.26.0

[2.27.0]: https://github.com/shipperstack/shipper/compare/2.26.2...2.27.0

# [2.26.2] - 2023-12-10

## Changed

- Fixed shipper sometimes placing invalid chunked uploads into a "limbo" state

[2.26.2]: https://github.com/shipperstack/shipper/compare/2.26.1...2.26.2

# [2.26.1] - 2023-12-07

## Changed

- Fixed the main page not sorting devices by name and enabled status
- Fixed bug where chunked upload would crash before finalizing the changes
- Changes to the site-wide configuration is now logged in the audit log
- Updated library dependencies (server)
  - django-ipware (6.0.1 -> 6.0.2)

[2.26.1]: https://github.com/shipperstack/shipper/compare/2.26.0...2.26.1

# [2.26.0] - 2023-11-30

## Added

- Added admin page for x86 types
- Added new OTA endpoint for x86 devices

## Changed

- shipper now checks for invalid configurations
- shipper now allows the x86_64 codename (in addition to the x86 codename)
- Updated library dependencies (server)
  - django-ipware (6.0.0 -> 6.0.1)
  - sentry-sdk (1.36.0 -> 1.38.0)
- Updated library dependencies (shippy)
  - sentry-sdk (1.36.0 -> 1.38.0)
- Updated translations
- Removed unnecessary dot from main server description
- Update default file name regex pattern
- General code cleanup

## Removed

- Removed deprecated configuration option for variants

[2.26.0]: https://github.com/shipperstack/shipper/compare/2.25.1...2.26.0

# [2.25.1] - 2023-11-23

## Changed

- Fixed the localization for the human-readable timedelta getting stuck on non-English languages

[2.25.1]: https://github.com/shipperstack/shipper/compare/2.25.0...2.25.1

# [2.25.0] - 2023-11-23

This release contains a database migration.

## Added

- Added preliminary x86 build support to shipper

## Changed

- Fixed timedelta string not being translated (#248)
- Updated help text in the admin page
- Build variants are now handled as database model objects
- General code cleanup

## Removed

- The variant configuration option has been deprecated and is slated for removal in the next release

[2.25.0]: https://github.com/shipperstack/shipper/compare/2.24.2...2.25.0

# [2.24.2] - 2023-11-23

This release contains a security vulnerability patch.

## Changed

- General code cleanup
- Updated library depndencies (server)
  - django-crispy-forms (2.0 -> 2.1)
  - @babel/traverse (7.22.10 -> 7.23.2) (security vulnerability patched)
  - django-ipware (5.0.1 -> 6.0.0)
  - crispy-bootstrap5 (0.7 -> 2023.10)
  - sentry-sdk (1.32.0 -> 1.36.0)
  - django (4.2.6 -> 4.2.7)
  - celery (5.3.4 -> 5.3.6)
  - humanize (4.8.0 -> 4.9.0)
- Updated library dependencies (release-helper)
  - rustix (0.38.7 -> 0.38.19)
- Updated library dependencies (shippy)
  - sentry-sdk (1.32.0 -> 1.36.0)
  - rich (13.6.0 -> 13.7.0)
  - setuptools (68.2.2 -> 69.0.2)
  - humanize (4.8.0 -> 4.9.0)

[2.24.2]: https://github.com/shipperstack/shipper/compare/2.24.1...2.24.2

# [2.24.1] - 2023-10-11

## Changed

- Fixed the archived flag for builds not working properly

[2.24.1]: https://github.com/shipperstack/shipper/compare/2.24.0...2.24.1

# [2.24.0] - 2023-10-11

## Added

- Added "archived builds" functionality. Archived builds are not mirrored and are subject to restrictions, such as reduced download speed

## Changed

- Updated library dependencies (server)
  - psycopg2-binary (2.9.7 -> 2.9.9)
  - django-ipware (5.0.0 -> 5.0.1)
  - django (4.2.5 -> 4.2.6)
  - sentry-sdk (1.31.0 -> 1.32.0)
- Updated library dependencies (shippy)
  - rich (13.5.3 -> 13.6.0)
  - semver (3.0.1 -> 3.0.2)
  - sentry-sdk (1.31.0 -> 1.32.0)
- Cleaned up API response error messages
- General code cleanup

## Removed

- Removed deprecated build counter API

[2.24.0]: https://github.com/shipperstack/shipper/compare/2.23.2...2.24.0

# [2.23.2] - 2023-09-18

## Changed

- Fixed shippy incorrectly initializing Sentry SDK for error reporting

[2.23.2]: https://github.com/shipperstack/shipper/compare/2.23.1...2.23.2

# [2.23.1] - 2023-09-18

## Changed

- Updated library dependencies (shippy)
  - rich (13.5.2 -> 13.5.3)
- Fixed OpenAPI schema generation crashing due to missing dependency

[2.23.1]: https://github.com/shipperstack/shipper/compare/2.23.0...2.23.1

# [2.23.0] - 2023-09-18

## Added

- Added search functionality to the build admin page
- Added filters to filter by download type for statistics
- Added task to clean up expired chunked upload
- Added OpenAPI schema generation

## Changed

- Updated library dependencies (shippy)
  - loguru (0.7.0 -> 0.7.2)
  - setuptools (68.1.2 -> 68.2.2)
  - sentry-sdk (1.30.0 -> 1.31.0)
- Updated library dependencies (server)
  - django (4.2.4 -> 4.2.5)
  - sentry-sdk (1.30.0 -> 1.31.0)
- Updated internal documentation for API endpoints
- General code cleanup

[2.23.0]: https://github.com/shipperstack/shipper/compare/2.22.2...2.23.0

# [2.22.2] - 2023-09-03

## Changed

- Updated library dependencies (server)
  - celery (5.3.3 -> 5.3.4)

[2.22.2]: https://github.com/shipperstack/shipper/compare/2.22.1...2.22.2

# [2.22.1] - 2023-09-03

- Fixed shippy checking for the latest version in the wrong repository

[2.22.1]: https://github.com/shipperstack/shipper/compare/2.22.0...2.22.1

# [2.22.0] - 2023-09-02

This release contains a database migration.

## Added

- Added a legacy mode toggle for mirror servers for resolving SSH issues

## Changed

- Updated library dependencies (server)
  - humanize (4.7.0 -> 4.8.0)
  - django-constance[database] (2.9.1 -> 3.1.0)
  - sentry-sdk (1.29.2 -> 1.30.0)
  - celery (5.3.1 -> 5.3.3)
- Updated library dependencies (shippy)
  - humanize (4.7.0 -> 4.8.0)
  - setuptools (68.0.0 -> 68.1.2)
  - sentry-sdk (1.29.2 -> 1.30.0)

[2.22.0]: https://github.com/shipperstack/shipper/compare/2.21.1...2.22.0

# [2.21.1] - 2023-08-15

## Changed

- Statistics items now list by new order
- Fixed download type not showing in the admin panel

[2.21.1]: https://github.com/shipperstack/shipper/compare/2.21.0...2.21.1

# [2.21.0] - 2023-08-15

This release contains a database migration.

## Added

- Added download type to statistics model
  All previous statistics will be set to the "download" type by default.
- Added v2 download build counter endpoint
- Added "latest" API endpoints (unstable!)

## Changed

- Removed workaround for bug in drf_chunked_upload
- Updated library dependencies (server)
  - drf-chunked-upload (0.5.1 -> 0.6.0)

[2.21.0]: https://github.com/shipperstack/shipper/compare/2.20.4...2.21.0

# [2.20.4] - 2023-08-11

## Changed

- Fixed webpack crashing and breaking the build process when git repo is unavailable

[2.20.4]: https://github.com/shipperstack/shipper/compare/2.20.3...2.20.4

# [2.20.3] - 2023-08-11

## Added

- Added a loading spinner to main downloads page

## Changed

- Updated base Docker image to Alpine 3.18
- Fixed main JS file being cached too aggressively with a cache-buster
- General code cleanup

[2.20.3]: https://github.com/shipperstack/shipper/compare/2.20.2...2.20.3

# [2.20.2] - 2023-08-10

## Changed

- Fixed server not building due to missing build dependencies

[2.20.2]: https://github.com/shipperstack/shipper/compare/2.20.1...2.20.2

# [2.20.1] - 2023-08-10

## Changed

- The search bar now fuzzy-searches through all devices
- The production build of the server project only installs production dependencies for the frontend
- General code cleanup

[2.20.1]: https://github.com/shipperstack/shipper/compare/2.20.0...2.20.1

# [2.20.0] - 2023-08-10

## Added

- Added a search bar to the main downloads page

## Changed

- Updated library dependencies (server)
  - psycopg2-binary (2.9.6 -> 2.9.7)
- Changed to use React for certain parts of the frontend (with more to come in the future!)

[2.20.0]: https://github.com/shipperstack/shipper/compare/2.19.1...2.20.0

# [2.19.1] - 2023-08-06

## Changed

- Fixed incorrect version string for server

[2.19.1]: https://github.com/shipperstack/shipper/compare/2.19.0...2.19.1

# [2.19.0] - 2023-08-02

## Changed

- Fixed the server crashing when API clients returned a bad build API parameter
- Fixed shippy sending the wrong build ID when disabling the build after an upload
- Fixed shippy not respecting shipper's rate limit response
- Updated library dependencies (server)
  - sentry-sdk (1.29.0 -> 1.29.2)
  - django (4.2.3 -> 4.2.4)
- Updated library dependencies (shippy)
  - rich (13.5.1 -> 13.5.2)
  - sentry-sdk (1.28.1 -> 1.29.2)
- General code cleanup

[2.19.0]: https://github.com/shipperstack/shipper/compare/2.18.3...2.19.0

# [2.18.3] - 2023-08-02

## Changed

- Fixed shippy crashing due to importing server compat version from the wrong file

[2.18.3]: https://github.com/shipperstack/shipper/compare/2.18.2...2.18.3

# [2.18.2] - 2023-08-02

## Added

- The raw variant name is shown in the build information

## Changed

- Fixed shippy crashing due to a missing version text file
- The main page device listing has proper margins
- Fixed the byte size information not showing on mouseover for build information
- General code cleanup
- Updated library dependencies (server)
  - sentry-sdk (1.28.1 -> 1.29.0)
  - paramiko (3.2.0 -> 3.3.1)
- Updated library dependencies (shippy)
  - rich (13.4.2 -> 13.5.1)

[2.18.2]: https://github.com/shipperstack/shipper/compare/2.18.1...2.18.2

# [2.18.1] - 2023-07-27

## Changed

- Fixed shippy crashing due to a missing version string file
- Fixed the "last updated" timedelta calculation not working
- Fixed the build timedelta calculation not working
- Updated translations for Korean
- Fixed translations not working properly
- Fixed cache middleware being set incorrectly
- General code cleanup

[2.18.1]: https://github.com/shipperstack/shipper/compare/2.18.0...2.18.1

# [2.18.0] - 2023-07-26

## Added

- Added "last updated" and "uploaded on" fields for the device and build pages on the webUI

## Changed

- Updated library dependencies (server)
  - gunicorn (20.1.0 -> 21.2.0)
- Fixed Docker mounting the SSH directory to mount as read-only
- Fixed server crashing when the supplied SSH key had incorrect permissions
- Version and date fields are now split on build page
- Checksums are now wrapped in code tags for better visibility

[2.18.0]: https://github.com/shipperstack/shipper/compare/2.17.0...2.18.0

# [2.17.0] - 2023-07-18

## Added

- Added mechanism to exclude the main server from the download mirror list

## Changed

- Fixed some code for shippy that was lost in the monorepo migration
- Updated library dependencies (shippy)
  - humanize (4.6.0 -> 4.7.0)
  - semver (3.0.0 -> 3.0.1)
  - rich (13.3.5 -> 13.4.2)
  - sentry-sdk (1.21.0 -> 1.28.1)
- General code cleanup
- shippy now logs network errors during login

[2.17.0]: https://github.com/shipperstack/shipper/compare/2.16.2...2.17.0

# [2.16.2] - 2023-07-17

## Changed

- Fixed a couple of bugs in the Docker subproject that occurred with the monorepo migration

[2.16.2]: https://github.com/shipperstack/shipper/compare/2.16.1...2.16.2

# [2.16.1] - 2023-07-17

## Added

- Added mechanism to download and use the photos directly for the device photos
- Added mechanism to potentially serve thumbhashes of device photos in the future
  (not fully implemented yet!)

## Changed

- shipper is now a monorepo! That means shippy, Docker files, and other helper scripts
  all live inside this repository.
- Fixed the hash names not being bold
- Aligned the first column in the build info table to the right
- Fixed no padding added to the build info table
- General code cleanup

[2.16.1]: https://github.com/shipperstack/shipper/compare/2.16.0...2.16.1

# [2.16.0] - 2023-07-14

## Added

- Added a redirect for the `.well-known` password change endpoint (#209)

## Changed

- Fixed a bug with the build delete view that caused it to delete devices, not builds 😱
- Fixed a bug that prevented "super"users from modifying build enable status
- The build download page has a better details layout
- Updated library dependencies
  - sentry-sdk (1.27.0 -> 1.28.1)
- General code cleanup

[2.16.0]: https://github.com/shipperstack/shipper/compare/2.15.1...2.16.0

# [2.15.1] - 2023-07-06

## Changed

- Fixed another mistaken crash with nonexistent builds in the internal admin build mirror status page

[2.15.1]: https://github.com/shipperstack/shipper/compare/2.15.0...2.15.1

# [2.15.0] - 2023-07-06

This release contains a security vulnerability patch.

## Changed

- Fixed a crash on nonexistent builds for the internal admin build mirror status page
- Updated library dependencies
  - sentry-sdk (1.26.0 -> 1.27.0)
  - django (4.2.2 -> 4.2.3)

[2.15.0]: https://github.com/shipperstack/shipper/compare/2.14.2...2.15.0

# [2.14.2] - 2023-07-04

## Changed

- Updated library dependencies
  - sentry-sdk (1.25.0 -> 1.26.0)
  - celery (5.2.7 -> 5.3.1)
  - django (4.2.1 -> 4.2.2)
  - django-cleanup (7.0.0 -> 8.0.0)
  - humanize (4.6.0 -> 4.7.0)

[2.14.2]: https://github.com/shipperstack/shipper/compare/2.14.1...2.14.2

# [2.14.1] - 2023-06-04

## Changed

- Fixed the statistics API crashing if the provided IP address was invalid
- Fixed disabled devices not getting the grayscale filter in the maintainer page
- Updated library dependencies
  - sentry-sdk(1.21.0 -> 1.25.0)
  - django (4.2 -> 4.2.1)
  - django-celery-results (2.5.0 -> 2.5.1)
  - django-auditlog (2.2.2 -> 2.3.0)
  - paramiko (3.1.0 -> 3.2.0)

[2.14.1]: https://github.com/shipperstack/shipper/compare/2.14.0...2.14.1

# [2.14.0] - 2023-04-30

## Added

- Added a field to the system API to show available variants for uploading builds

[2.14.0]: https://github.com/shipperstack/shipper/compare/2.13.2...2.14.0

# [2.13.2] - 2023-04-28

## Changed

- Fixed a permission issue with all internal admin pages

[2.13.2]: https://github.com/shipperstack/shipper/compare/2.13.1...2.13.2

# [2.13.1] - 2023-04-28

## Changed

- Fixed a bug with the backend task result cleaning task

[2.13.1]: https://github.com/shipperstack/shipper/compare/2.13.0...2.13.1

# [2.13.0] - 2023-04-28

This release contains new configuration keys.

## Added

- Added support for memcached

## Changed

- Fixed a caching issue on the internal admin pages. Internal admin pages are no longer cached
- Cache timeouts are now 30 seconds instead of 5 minutes
- General code cleanup
- Celery tasks can now run up to 30 minutes
- Built-in tasks for shipper now run periodically automatically, no configuration required
- Fixed some styling issues on the build mirror status admin page

[2.13.0]: https://github.com/shipperstack/shipper/compare/2.12.7...2.13.0

# [2.12.7] - 2023-04-28

## Added

- Added more information to the build mirror status page

## Changed

- Fixed a bug where successful mirrors would show an empty progress bar on the status page
- Cleaned up unnecessary remnants from the build mirror status page template

[2.12.7]: https://github.com/shipperstack/shipper/compare/2.12.6...2.12.7

# [2.12.6] - 2023-04-28

## Changed

- Fixed the broken table in the build mirror status page

[2.12.6]: https://github.com/shipperstack/shipper/compare/2.12.5...2.12.6

# [2.12.5] - 2023-04-28

## Changed

- Fixed the build mirror status page causing a 500 error

[2.12.5]: https://github.com/shipperstack/shipper/compare/2.12.4...2.12.5

# [2.12.4] - 2023-04-28

## Changed

- Fixed the build mirror status page causing a 500 error

[2.12.4]: https://github.com/shipperstack/shipper/compare/2.12.3...2.12.4

# [2.12.3] - 2023-04-28

## Changed

- Fixed the build mirror status page causing a 500 error

[2.12.3]: https://github.com/shipperstack/shipper/compare/2.12.2...2.12.3

# [2.12.2] - 2023-04-28

## Changed

- Fixed the build mirror status page causing a 500 error

[2.12.2]: https://github.com/shipperstack/shipper/compare/2.12.1...2.12.2

# [2.12.1] - 2023-04-28

## Changed

- Fixed an improper configuration issue stemming from the internal admin

[2.12.1]: https://github.com/shipperstack/shipper/compare/2.12.0...2.12.1

# [2.12.0] - 2023-04-28

## Added

- Added a new build mirror status page for admins

## Changed

- Fixed the admin URLs being broken
- Changed the default admin endpoint from `admins/` to `admin/`

[2.12.0]: https://github.com/shipperstack/shipper/compare/2.11.5...2.12.0

# [2.11.5] - 2023-04-27

## Changed

- Fixed the "All" option appearing twice in the filter list
- Fixed a crash when invoking checksum generation

[2.11.5]: https://github.com/shipperstack/shipper/compare/2.11.4...2.11.5

# [2.11.4] - 2023-04-27

## Changed

- Fixed a bug where no builds would show up on the admin view if certain filters weren't enabled

[2.11.4]: https://github.com/shipperstack/shipper/compare/2.11.3...2.11.4

# [2.11.3] - 2023-04-27

## Changed

- Fixed a bug where no builds would show up on the admin view

[2.11.3]: https://github.com/shipperstack/shipper/compare/2.11.2...2.11.3

# [2.11.2] - 2023-04-27

## Added

- Added more build filtering options to the admin view

[2.11.2]: https://github.com/shipperstack/shipper/compare/2.11.1...2.11.2

# [2.11.1] - 2023-04-27

## Changed

- Fixed certain tasks not being routed to the correct queue
- Updated library dependencies
  - sentry-sdk (1.19.1 -> 1.21.0)

[2.11.1]: https://github.com/shipperstack/shipper/compare/2.11.0...2.11.1

# [2.11.0] - 2023-04-10

## Added

- Added a new Celery queue to separate long-running build mirror tasks

## Changed

- Fixed a bug that caused a task to run even if another instance was running
- The build mirror task now respects the soft time limit imposed by Celery
- Fixed a bug in an unused function intended for a future release (coming soon!)
- General code cleanup

[2.11.0]: https://github.com/shipperstack/shipper/compare/2.10.4...2.11.0

# [2.10.4] - 2023-04-09

## Changed

- Fixes a 500 server error due to a templating error

[2.10.4]: https://github.com/shipperstack/shipper/compare/2.10.3...2.10.4

# [2.10.3] - 2023-04-09

## Changed

- Fixes a 500 server error when visiting the device downloads page

[2.10.3]: https://github.com/shipperstack/shipper/compare/2.10.2...2.10.3

# [2.10.2] - 2023-04-09

## Changed

- Updated translations for Korean
- Made more strings translatable
- Updated library dependencies
  - sentry-sdk (1.18.0 -> 1.19.1)

[2.10.2]: https://github.com/shipperstack/shipper/compare/2.10.1...2.10.2

# [2.10.1] - 2023-04-04

## Changed

- Updated library dependencies
  - django (4.1.7 -> 4.2)
  - psycopg2-binary (2.9.5 -> 2.9.6)

[2.10.1]: https://github.com/shipperstack/shipper/compare/2.10.0...2.10.1

# [2.10.0] - 2023-04-01

## Changed

- Fixed too many build mirroring tasks running at once and all timing out
- Updated library dependencies
  - sentry-sdk (1.17.0 -> 1.18.0)

[2.10.0]: https://github.com/shipperstack/shipper/compare/2.9.19...2.10.0

# [2.9.19] - 2023-03-30

## Changed

- Fixed build mirroring task crashing on start

[2.9.19]: https://github.com/shipperstack/shipper/compare/2.9.18...2.9.19

# [2.9.18] - 2023-03-30

## Changed

- Fixed build mirroring task recording success results, even when it failed

## Removed

- Removed timeout signals from build mirroring task as they never worked correctly

[2.9.18]: https://github.com/shipperstack/shipper/compare/2.9.17...2.9.18

# [2.9.17] - 2023-03-30

## Added

- Added debug logging to the build mirroring task

[2.9.17]: https://github.com/shipperstack/shipper/compare/2.9.16...2.9.17

# [2.9.16] - 2023-03-29

## Changed

- Fixed a bug with the timeout handler in the build mirroring task
- Fixed a bug with the exception handler in the build mirroring task

[2.9.16]: https://github.com/shipperstack/shipper/compare/2.9.15...2.9.16

# [2.9.15] - 2023-03-29

## Changed

- Fixed a bug with the timeout handler in the build mirroring task

[2.9.15]: https://github.com/shipperstack/shipper/compare/2.9.14...2.9.15

# [2.9.14] - 2023-03-29

## Changed

- Fixed a bug with the timeout handler in the build mirroring task

[2.9.14]: https://github.com/shipperstack/shipper/compare/2.9.13...2.9.14

# [2.9.13] - 2023-03-29

## Changed

- Fixed a bug with the timeout handler in the build mirroring task

[2.9.13]: https://github.com/shipperstack/shipper/compare/2.9.12...2.9.13

# [2.9.12] - 2023-03-29

## Changed

- Fixed a bug with the timeout handler in the build mirroring task

[2.9.12]: https://github.com/shipperstack/shipper/compare/2.9.11...2.9.12

# [2.9.11] - 2023-03-29

## Changed

- Fixed a bug with the homemade timeout handler function inside the build mirroring task

## Removed

- Removed an unused debug configuration option

[2.9.11]: https://github.com/shipperstack/shipper/compare/2.9.10...2.9.11

# [2.9.10] - 2023-03-29

## Changed

- Fixed the build mirroring task overwriting the failure result in the Celery results database
- Fixed the build mirroring task crashing because of an invalid state
- General code cleanup

# [2.9.9] - 2023-03-28

## Changed

- Backend tests for not overwriting Celery task states

# [2.9.8] - 2023-03-27

## Changed

- Fixed a bug that prevented build mirroring from working

# [2.9.7] - 2023-03-26

## Added

- Added debugging mechanism to disable progress updates for the Celery upload task

## Changed

- General code cleanup
- Updated library dependencies
  - paramiko (3.0.0 -> 3.1.0)

# [2.9.6] - 2023-03-18

## Changed

- Fixed handling exceptions during SFTP upload to mirror servers
- Updated library dependencies
  - sentry-sdk (1.15.0 -> 1.17.0)
  - django-celery-results (2.4.0 -> 2.5.0)
  - django-celery-beat (2.4.0 -> 2.5.0)

# [2.9.5] - 2023-02-25

## Changed

- Fixed task information not showing up under Celery results table

# [2.9.4] - 2023-02-25

## Changed

- Celery tasks now update their progress state
- Celery tasks now show that they have been started, when they are started, instead of remaining at pending
- Celery now uses the default Django backend for caching
- Updated library dependencies
  - humanize (4.5.0 -> 4.6.0)
  - sentry-sdk (1.14.0 -> 1.15.0)
  - django (4.1.6 -> 4.1.7)
  - django-cleanup (6.0.0 -> 7.0.0)
  - django-crispy-forms (1.14.0 -> 2.0)

# [2.9.3] - 2023-02-02

## Changed

- Updated library dependencies
  - sentry-sdk (1.12.1 -> 1.14.0)
  - django-auditlog (2.2.1 -> 2.2.2)
  - paramiko (2.12.0 -> 3.0.0)
  - django (4.1.5 -> 4.1.6)
  - humanize (4.4.0 -> 4.5.0)

# [2.9.2] - 2023-01-08

## Added

- Added general API endpoint to list active maintainers only

## Changed

- The admin page now shows user-editable fields for maintainers
- `KeyboardInterrupt` errors are now ignored by Sentry
- The general API endpoint that returns all maintainers now has an `active` field
- Fixed chunked upload API endpoint returning stale responses
- Updated library dependencies
  - django (4.1.4 -> 4.1.5)

# [2.9.1] - 2022-12-30

## Changed

- Fixed static files being deleted during server setup

# [2.9.0] - 2022-12-30

## Added

- Added more account fields for users (maintainers)
- Added account details edit page
- Added API endpoint to list maintainer details

## Changed

- Form pages in shipper now look snazzier, thanks to `django-crispy-forms`!
- Updated library dependencies
  - django (4.1.3 -> 4.1.4)
  - sentry-sdk (1.11.1 -> 1.12.1)
- shipper is now licensed under AGPLv3!
- Miscellaneous code improvements
- General code cleanup

# [2.8.0] - 2022-12-03

This release contains a database migration.

## Changed

- Updated library dependencies
  - sentry-sdk (1.11.0 -> 1.11.1)
  - django-auditlog (2.2.0 -> 2.2.1)
- The Statistics model now infers the device directly from the Build model field

# [2.7.1] - 2022-11-23

## Changed

- Updated library dependencies
  - sentry-sdk (1.10.1 -> 1.11.0)
  - django-auditlog (2.1.1 -> 2.2.0)
  - paramiko (2.11.0 -> 2.12.0)

# [2.7.0] - 2022-11-01

This release contains a security vulnerability patch.

## Changed

- Updated library dependencies
  - sentry-sdk (1.9.9 -> 1.10.1)
  - psycopg2-binary (2.9.3 -> 2.9.5)
  - django-celery-beat (2.3.0 -> 2.4.0)

# [2.6.1] - 2022-09-30

## Changed

- Updated library dependencies
  - humanize (4.3.0 -> 4.4.0)
  - sentry-sdk (1.9.8 -> 1.9.9)
  - djangorestframework (3.13.1 -> 3.14.0)
  - django-dbbackup (4.0.1 -> 4.0.2)

# [2.6.0] - 2022-09-09

This release contains a new configuration key.
This release contains a security vulnerability patch.

## Added

- Added django-dbbackup for backing up shipper instance

## Changed

- Updated library dependencies
  - django (4.0.6 -> 4.0.7)
  - sentry-sdk (1.9.2 -> 1.9.8)
  - humanize (4.2.3 -> 4.3.0)
  - django-constance[database] (2.9.0 -> 2.9.1)

# [2.5.2] - 2022-08-06

## Changed

- Updated library dependencies
  - sentry-sdk (1.6.0 -> 1.9.2)
  - django-auditlog (2.1.0 -> 2.1.1)

# [2.5.1] - 2022-07-05

## Changed

- Updated library dependencies
  - sentry-sdk (1.5.12 -> 1.6.0)
  - humanize (4.1.0 -> 4.2.3)
  - django-celery-results (2.3.1 -> 2.4.0)
  - django-auditlog (2.0.0 -> 2.1.0)
  - django (4.0.5 -> 4.0.6)

# [2.5.0] - 2022-06-18

## Added

- Added an "allowed versions" configuration option to limit what versions can be uploaded to the server
- Added a placeholder image for devices without images

## Changed

- Moved Django admin to `django-admin/` path
- Admin pages now live under `admin/`
- General code cleanup

# [2.4.0] - 2022-06-13

This release contains a database migration.

## Added

- Added a new "full access" field in the account model, that allows access to all devices

## Changed

- Squashed migration is now the default migration

## Removed

- Removed previous migrations before the squash. Make sure to have the squashed migration in your migration history in your database, or upgrade to a release that has the previous migrations (2.2.0 ~ 2.3.0) before upgrading to this release
- Removed command to make a user a "full user"

# [2.3.0] - 2022-06-11

This release contains a new configuration key.

## Added

- Added a new configuration key (`SHIPPER_CSRF_TRUSTED_ORIGINS`) to fix authentication errors due to CSRF

# [2.2.1] - 2022-06-11

## Changed

- Fixed a bug with the migration to the `maintainer` app that prevented the entire server from starting properly

# [2.2.0] - 2022-06-11

This release contains a database migration.

## Changed

- Squashed migrations in the `core` app. You must upgrade to this version before upgrading further as the next release will not contain the previous migrations
- Fixed a bug with Sentry SDK PII configuration not taking effect
- General code cleanup
- Updated library dependencies
  - django-celery-beat (2.2.1 -> 2.3.0)
  - Django (3.2.13 -> 4.0.5)

## Removed

- Removed Python 3.7 support because Django 4.x does not support it

# [2.1.0] - 2022-06-08

## Removed

- Removed the intermediate `django_rename_app` library. You must first upgrade to 2.0.0 if upgrading from a previous release

# [2.0.0] - 2022-06-07

This release requires a manual migration. Please [read the documentation for more information.](docs/sysadmin/Upgrading.md#-1163)

## Changed

- Renamed `shipper` app to `core` for better code organization
- Unsupported devices are now grayed out on the main screen
- Updated library dependencies
  - celery (5.2.6 -> 5.2.7)

[2.9.11]: https://github.com/shipperstack/shipper/compare/2.9.10...2.9.11
[2.9.10]: https://github.com/shipperstack/shipper/compare/2.9.9...2.9.10
[2.9.9]: https://github.com/shipperstack/shipper/compare/2.9.8...2.9.9
[2.9.8]: https://github.com/shipperstack/shipper/compare/2.9.7...2.9.8
[2.9.7]: https://github.com/shipperstack/shipper/compare/2.9.6...2.9.7
[2.9.6]: https://github.com/shipperstack/shipper/compare/2.9.5...2.9.6
[2.9.5]: https://github.com/shipperstack/shipper/compare/2.9.4...2.9.5
[2.9.4]: https://github.com/shipperstack/shipper/compare/2.9.3...2.9.4
[2.9.3]: https://github.com/shipperstack/shipper/compare/2.9.2...2.9.3
[2.9.2]: https://github.com/shipperstack/shipper/compare/2.9.1...2.9.2
[2.9.1]: https://github.com/shipperstack/shipper/compare/2.9.0...2.9.1
[2.9.0]: https://github.com/shipperstack/shipper/compare/2.8.0...2.9.0
[2.8.0]: https://github.com/shipperstack/shipper/compare/2.7.1...2.8.0
[2.7.1]: https://github.com/shipperstack/shipper/compare/2.7.0...2.7.1
[2.7.0]: https://github.com/shipperstack/shipper/compare/2.6.1...2.7.0
[2.6.1]: https://github.com/shipperstack/shipper/compare/2.6.0...2.6.1
[2.6.0]: https://github.com/shipperstack/shipper/compare/2.5.2...2.6.0
[2.5.2]: https://github.com/shipperstack/shipper/compare/2.5.1...2.5.2
[2.5.1]: https://github.com/shipperstack/shipper/compare/2.5.0...2.5.1
[2.5.0]: https://github.com/shipperstack/shipper/compare/2.4.0...2.5.0
[2.4.0]: https://github.com/shipperstack/shipper/compare/2.3.0...2.4.0
[2.3.0]: https://github.com/shipperstack/shipper/compare/2.2.1...2.3.0
[2.2.1]: https://github.com/shipperstack/shipper/compare/2.2.0...2.2.1
[2.2.0]: https://github.com/shipperstack/shipper/compare/2.1.0...2.2.0
[2.1.0]: https://github.com/shipperstack/shipper/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/shipperstack/shipper/compare/1.16.3...2.0.0

---

<details>

<summary>1.x.x changelog</summary>

# [1.16.3] - 2022-05-22

## Changed

- Fixed a bug in the model returning an incorrect exception

# [1.16.2] - 2022-05-22

## Added

- shipper now has a proper FOSS license - GPLv3!

## Changed

- shipper does not send TimeLimitExceeded exceptions to Sentry anymore
- Fixed a bug with the API checking the list of available builds for a given variant
- Updated filename regex pattern defaults to support device codenames with numerical values and underscores
- Updated library dependencies
  - django-constance[database] (2.8.0 -> 2.9.0)
  - paramiko (2.10.4 -> 2.11.0)

## Removed

- Removed Docker-related files. Check them out [at the shipperstack/shipper-docker][shipper-docker-repo-url] repository
- Removed the documentation website. Documentation exists as Markdown files inside the `docs/` directory

[shipper-docker-repo-url]: https://github.com/shipperstack/shipper-docker/

# [1.16.1] - 2022-05-12

This release re-adds a configuration key.

## Changed

- Moved the `SHIPPER_UPLOAD_CHECKSUM` configuration key back to the static configuration file.
- Updated library dependencies
  - sentry-sdk (1.5.11 -> 1.5.12)

# [1.16.0] - 2022-05-11

This release contains a database migration.
This release migrates some configuration keys.

## Added

- Added new dynamic configuration option in the admin page, thanks to django-constance

## Changed

- Fixed "Statistics" model in admin page having an incorrect extra s postfix in the end
- Ignore ConnectionRefusedError in Celery workers from consideration for sending to Sentry
- (Finally) fixed CSS rule to properly wrap long checksum values on mobile (#82)
- Updated library dependencies
  - django-auditlog (1.0.0 -> 2.0.0)
- General code cleanup

## Removed

- Removed some configuration keys that have moved to the admin page

# [1.15.6] - 2022-05-04

This release contains a database migration.

## Changed

- Add unique constraint to codename field in Device. Before upgrading, make sure there are no duplicate codenames in the Device table (see "Upgrading" page on documentation for more information)
- Updated library dependencies
  - humanize (4.0.0 -> 4.1.0)
  - sentry-sdk (1.5.10 -> 1.5.11)

# [1.15.5] - 2022-05-01

## Changed

- Fixed a typo that broke querying builds from the database

# [1.15.4] - 2022-05-01

## Changed

- Fixed a bug that caused a 500 server error on the main page
- Fixed SFTP uploads uploading to the wrong directory

# [1.15.3] - 2022-05-01

## Changed

- Fixed styling bug on mobile where long checksum values would overflow the width of the screen (#82)
- Fixed non-hashed builds showing up in the API (#83)
- Fixed a bug with the mirroring task where a nonexistent MD5 checksum file would be considered for upload

# [1.15.2] - 2022-04-30

## Changed

- Fixed a bug with paramiko authentication preventing build mirroring

# [1.15.1] - 2022-04-30

This release contains an API change.

## Changed

- shipper now correctly generates MD5 values when scanning for builds that do not have checksums generated yet
- Fixed a bug with the LOS-style updater API looking for the nonexistent MD5 file
- General code cleanup

# [1.15.0] - 2022-04-30

This release contains a database migration.
This release contains a security vulnerability patch.
This release contains a new configuration key.

## Added

- Added a new configuration key to set checksum value expected by server

## Changed

- shipper now accepts different checksum types from shippy
- General code cleanup
- Updated library dependencies
  - Django (3.2.12 -> 3.2.13)
  - django-celery-results (2.3.0 -> 2.3.1)
  - paramiko (2.10.3 -> 2.10.4)

## Removed

- Removed MD5 checksum file field from Build object in database
- Removed dependency on pysftp as it is outdated and has an authentication problem. shipper now uses paramiko directly

# [1.14.3] - 2022-04-19

## Added

- Added new language switching option in navigation bar
- shipper now displays compatible shippy versions to clients

## Changed

- General code cleanup
- Updated library dependencies
  - sentry-sdk (1.5.6 -> 1.5.10)
  - django-celery-results (2.2.0 -> 2.3.0)
  - celery (5.2.3 -> 5.2.6)

## Removed

- RegexParseException has been removed in favor of UploadException

# [1.14.2] - 2022-02-27

This release contains a configuration key change.

## Added

- Added a statistics admin view to see all statistic entries

## Changed

- Fixed a bug that prevented uploads with shippy

# [1.14.1] - 2022-02-26

## Added

- Added a missing dependency in Docker that prevented translations from being compiled properly

## Changed

- Fixed a bug with the debug tag that was causing a 500 server error for all pages

# [1.14.0] - 2022-02-26

This release contains a database migration.
This release contains a security vulnerability patch.
This release contains a configuration key change.

## Added

- Added functionality to regex match the uploaded build artifact filename
- Added configuration keys for the regex match pattern
- Added localization mechanism for shipper
- Added API endpoint to fetch the regex match pattern
- Added cache mechanism configuration to reduce server load

## Changed

- Fixed upload API to delete chunked build if the device does not exist
- Changed statistics model to be more generic
- General code cleanup
- Updated library dependencies

## Removed

- Removed redundant configuration key (`SHIPPER_FILE_NAME_FORMAT_DELIMITER`)

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

[1.16.3]: https://github.com/shipperstack/shipper/compare/1.16.2...1.16.3
[1.16.2]: https://github.com/shipperstack/shipper/compare/1.16.1...1.16.2
[1.16.1]: https://github.com/shipperstack/shipper/compare/1.16.0...1.16.1
[1.16.0]: https://github.com/shipperstack/shipper/compare/1.15.6...1.16.0
[1.15.6]: https://github.com/shipperstack/shipper/compare/1.15.5...1.15.6
[1.15.5]: https://github.com/shipperstack/shipper/compare/1.15.4...1.15.5
[1.15.4]: https://github.com/shipperstack/shipper/compare/1.15.3...1.15.4
[1.15.3]: https://github.com/shipperstack/shipper/compare/1.15.2...1.15.3
[1.15.2]: https://github.com/shipperstack/shipper/compare/1.15.1...1.15.2
[1.15.1]: https://github.com/shipperstack/shipper/compare/1.15.0...1.15.1
[1.15.0]: https://github.com/shipperstack/shipper/compare/1.14.3...1.15.0
[1.14.3]: https://github.com/shipperstack/shipper/compare/1.14.2...1.14.3
[1.14.2]: https://github.com/shipperstack/shipper/compare/1.14.1...1.14.2
[1.14.1]: https://github.com/shipperstack/shipper/compare/1.14.0...1.14.1
[1.14.0]: https://github.com/shipperstack/shipper/compare/1.13.6...1.14.0
[1.13.6]: https://github.com/shipperstack/shipper/compare/1.13.5...1.13.6
[1.13.5]: https://github.com/shipperstack/shipper/compare/1.13.4...1.13.5
[1.13.4]: https://github.com/shipperstack/shipper/compare/1.13.3...1.13.4
[1.13.3]: https://github.com/shipperstack/shipper/compare/1.13.2...1.13.3
[1.13.2]: https://github.com/shipperstack/shipper/compare/1.13.1...1.13.2
[1.13.1]: https://github.com/shipperstack/shipper/compare/1.13.0...1.13.1
[1.13.0]: https://github.com/shipperstack/shipper/compare/1.12.0...1.13.0
[1.12.0]: https://github.com/shipperstack/shipper/compare/1.11.2...1.12.0
[1.11.2]: https://github.com/shipperstack/shipper/compare/1.11.1...1.11.2
[1.11.1]: https://github.com/shipperstack/shipper/compare/1.11.0...1.11.1
[1.11.0]: https://github.com/shipperstack/shipper/compare/1.10.3...1.11.0
[1.10.3]: https://github.com/shipperstack/shipper/compare/1.10.2...1.10.3
[1.10.2]: https://github.com/shipperstack/shipper/compare/1.10.1...1.10.2
[1.10.1]: https://github.com/shipperstack/shipper/compare/1.10.0...1.10.1
[1.10.0]: https://github.com/shipperstack/shipper/compare/1.9.16...1.10.0
[1.9.16]: https://github.com/shipperstack/shipper/compare/1.9.15...1.9.16
[1.9.15]: https://github.com/shipperstack/shipper/compare/1.9.14...1.9.15
[1.9.14]: https://github.com/shipperstack/shipper/compare/1.9.13...1.9.14
[1.9.13]: https://github.com/shipperstack/shipper/compare/1.9.12...1.9.13
[1.9.12]: https://github.com/shipperstack/shipper/compare/1.9.11...1.9.12
[1.9.11]: https://github.com/shipperstack/shipper/compare/1.9.10...1.9.11
[1.9.10]: https://github.com/shipperstack/shipper/compare/1.9.9...1.9.10
[1.9.9]: https://github.com/shipperstack/shipper/compare/1.9.8...1.9.9
[1.9.8]: https://github.com/shipperstack/shipper/compare/1.9.7...1.9.8
[1.9.7]: https://github.com/shipperstack/shipper/compare/1.9.6...1.9.7
[1.9.6]: https://github.com/shipperstack/shipper/compare/1.9.5...1.9.6
[1.9.5]: https://github.com/shipperstack/shipper/compare/1.9.4...1.9.5
[1.9.4]: https://github.com/shipperstack/shipper/compare/1.9.3...1.9.4
[1.9.3]: https://github.com/shipperstack/shipper/compare/1.9.2...1.9.3
[1.9.2]: https://github.com/shipperstack/shipper/compare/1.9.1...1.9.2
[1.9.1]: https://github.com/shipperstack/shipper/compare/1.9.0...1.9.1
[1.9.0]: https://github.com/shipperstack/shipper/compare/1.8.3...1.9.0
[1.8.3]: https://github.com/shipperstack/shipper/compare/1.8.2...1.8.3
[1.8.2]: https://github.com/shipperstack/shipper/compare/1.8.1...1.8.2
[1.8.1]: https://github.com/shipperstack/shipper/compare/1.8.0...1.8.1
[1.8.0]: https://github.com/shipperstack/shipper/compare/1.7.4...1.8.0
[1.7.4]: https://github.com/shipperstack/shipper/compare/1.7.3...1.7.4
[1.7.3]: https://github.com/shipperstack/shipper/compare/1.7.2...1.7.3
[1.7.2]: https://github.com/shipperstack/shipper/compare/1.7.1...1.7.2
[1.7.1]: https://github.com/shipperstack/shipper/compare/1.7.0...1.7.1
[1.7.0]: https://github.com/shipperstack/shipper/compare/1.6.16...1.7.0
[1.6.16]: https://github.com/shipperstack/shipper/compare/1.6.15...1.6.16
[1.6.15]: https://github.com/shipperstack/shipper/compare/1.6.14...1.6.15
[1.6.14]: https://github.com/shipperstack/shipper/compare/1.6.13...1.6.14
[1.6.13]: https://github.com/shipperstack/shipper/compare/1.6.12...1.6.13
[1.6.12]: https://github.com/shipperstack/shipper/compare/1.6.11...1.6.12
[1.6.11]: https://github.com/shipperstack/shipper/compare/1.6.10...1.6.11
[1.6.10]: https://github.com/shipperstack/shipper/compare/1.6.9...1.6.10
[1.6.9]: https://github.com/shipperstack/shipper/compare/1.6.8...1.6.9
[1.6.8]: https://github.com/shipperstack/shipper/compare/1.6.7...1.6.8
[1.6.7]: https://github.com/shipperstack/shipper/compare/1.6.6...1.6.7
[1.6.6]: https://github.com/shipperstack/shipper/compare/1.6.5...1.6.6
[1.6.5]: https://github.com/shipperstack/shipper/compare/1.6.4...1.6.5
[1.6.4]: https://github.com/shipperstack/shipper/compare/1.6.3...1.6.4
[1.6.3]: https://github.com/shipperstack/shipper/compare/1.6.2...1.6.3
[1.6.2]: https://github.com/shipperstack/shipper/compare/1.6.1...1.6.2
[1.6.1]: https://github.com/shipperstack/shipper/compare/1.6.0...1.6.1
[1.6.0]: https://github.com/shipperstack/shipper/compare/1.5.3...1.6.0
[1.5.3]: https://github.com/shipperstack/shipper/compare/1.5.2...1.5.3
[1.5.2]: https://github.com/shipperstack/shipper/compare/1.5.1...1.5.2
[1.5.1]: https://github.com/shipperstack/shipper/compare/1.5.0...1.5.1
[1.5.0]: https://github.com/shipperstack/shipper/compare/1.4.4...1.5.0
[1.4.4]: https://github.com/shipperstack/shipper/compare/1.4.3...1.4.4
[1.4.3]: https://github.com/shipperstack/shipper/compare/1.4.2...1.4.3
[1.4.2]: https://github.com/shipperstack/shipper/compare/1.4.1...1.4.2
[1.4.1]: https://github.com/shipperstack/shipper/compare/1.4.0...1.4.1
[1.4.0]: https://github.com/shipperstack/shipper/compare/1.3.1...1.4.0
[1.3.1]: https://github.com/shipperstack/shipper/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/shipperstack/shipper/compare/1.2.5...1.3.0
[1.2.5]: https://github.com/shipperstack/shipper/compare/1.2.4...1.2.5
[1.2.4]: https://github.com/shipperstack/shipper/compare/1.2.3...1.2.4
[1.2.3]: https://github.com/shipperstack/shipper/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/shipperstack/shipper/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/shipperstack/shipper/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/shipperstack/shipper/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/shipperstack/shipper/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/shipperstack/shipper/compare/85a2753f7f234052b8bdf28e0dae98e5042fb99d...1.0.0

</details>
