# API

This page documents the API endpoints exposed by shipper.

## Latest endpoints

### Warning!

The latest API schema is obviously not stable and can change at any time. Please proceed with caution when using these API endpoints, and keep in mind that they may change in functionality/usage and/or may disappear in the future.

Currently, all latest endpoints map to the v1 endpoints, except for the statistics build counter, which maps to v2. In the future, as more API revisions are released, the latest endpoint mapping will be updated without notice. Therefore, do not use this endpoint in production!

If you designed something around the latest endpoint (such as `https://host/api/latest/download/build/counter/`), in order to "production-alize" it, use the version-mapped endpoint that the latest endpoint maps to (in this case, it would be `https://host/api/v2/download/build/counter/`).

## v2 endpoints

### Statistics

 - `https://host/api/v2/download/build/counter/`

Increments the download count of a given build. This API should be called by the OTA system whenever a user downloads a build. Either the `file_name` field or the `build_id` field must be supplied via REST. The `download_type` field must also be supplied, and it can currently either be `download` or `update`.

If the user is installing the build for the first time (i.e. they are downloading the build from your app to install on their device), then the download type should be `download`. If the user is obtaining the build through an OTA app, then the download type should be `update`. The endpoint will throw a 400 if a different download type is given.

This endpoint will throw a 404 if a build with the given file name or build ID does not exist, with specific error messages for each scenario.


### shippy

 - `https://host/api/v2/system/info/`

Returns the shipper version installed on the server.


## v1 endpoints

### Statistics

 - `https://host/api/v1/download/build/counter/`

#### This endpoint has been deprecated for v2. It will be removed at some point in the future!

Increments the download count of a given build. This API should be called by the OTA system whenever a user downloads a build. Either the `file_name` field or the `build_id` field must be supplied via REST.

This endpoint will throw a 404 if a build with the given file name or build ID does not exist, with specific error messages for each scenario.

 - `https://host/api/v1/download/count/day/`

Returns the number of downloads shipper has served in the last 24 hours.

 - `https://host/api/v1/download/count/week/`

Returns the number of downloads shipper has served in the last 7 days.

 - `https://host/api/v1/download/count/month/`

Returns the number of downloads shipper has served in the last 31 days.

 - `https://host/api/v1/download/count/all/`

Returns the number of downloads shipper has served, all time.

### shippy

The following endpoints are used by [shippy, a tool to help maintainers upload builds to shipper.](https://github.com/ericswpark/shippy)

 - `https://host/api/v1/system/info/`

 #### This endpoint has been deprecated for v2. It will be removed at some point in the future!

Returns the shipper version installed on the server.

 - `https://host/api/v1/maintainers/login/`

Returns an authentication token when the correct username and password is supplied. The `username` and `password` fields must be supplied via REST.

This endpoint will throw a 400 if either the `username` or `password` field is blank and a 404 if the credentials are invalid.

 - `https://host/api/v1/maintainers/token_check/`

Checks if a REST authentication token is still valid and returns the username of the token bearer if it is. The authentication token must be supplied in the REST header.

 - `https://host/api/v1/maintainers/upload_filename_regex_pattern`

Returns the regex pattern used to match uploaded build artifacts. The authentication token must be supplied in the REST header.

 - `https://host/api/v1/maintainers/device/chunked_upload/`

Allows you to upload a build object in chunks given the build file and the corresponding checksum. Multiple fields must be supplied via REST. The authentication token must be supplied in the REST header. This endpoint only accepts the initial chunk, and subsequent chunks must be sent using the endpoint below. Please refer to the shippy project for implementation details.

 - `https://host/api/v1/maintainers/device/chunked_upload/<uuid:pk>`

Allows you to upload the rest of the build object by sending subsequent chunks associated with the chunked upload ID. Multiple fields must be supplied via REST. The authentication token must be supplied in the REST header. Please refer to the shippy project for implementation details.

 - `https://host/api/v1/maintainers/build/enabled_status_modify/`

Allows you to enable/disable a build object. The `build_id` and `enable` fields must be supplied via REST. The authentication token must be supplied in the REST header.

Returns a 200 with the enable/disable status if successful.

This endpoint will throw a 400 if one or more of the required fields are missing and a 401 if you are unauthorized to modify builds.

### Updater

 - `https://host/api/v1/updater/los/<slug:codename>/<slug:variant>/`

This fetches all build objects for the device with the specified `codename` and `variant` slug. There are four possible `variant` slugs: `gapps`, `vanilla` (non-GApps), `foss`, and `goapps` (Go Apps).

This endpoint will throw a 404 if the device is not found or if there are no builds for the specified variant and a 400 if the supplied variant name is invalid.

### General

These are general endpoints used to query information on devices and builds.

 - `https://host/api/v1/general/device/all/`

Shows the list of available devices, their associated codenames, and the variants available for download.

 - `https://host/api/v1/general/build/latest/<slug:codename>/<slug:variant>/`

Returns the latest build for the given device codename and variant.

This endpoint will throw a 404 if the specified device does not exist or if no builds exist for the specified variant yet, with respective error messages for each.
