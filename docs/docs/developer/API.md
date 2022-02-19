# Warning!
shipper/shippy's API schema is not stable and can change at any time. Please proceed with caution when using these API endpoints, and keep in mind that they may change or disappear in the future.

# v1 endpoints

## Statistics

 - `https://host/api/v1/download/build/counter/`

Increments the download count of a given build. This API should be called by the OTA system whenever a user downloads a build. Either the `file_name` field or the `build_id` field must be supplied via REST.

This endpoint will throw a 404 if a build with the given file name or build ID does not exist, with specific error messages for each scenario.

 - `https://host/api/v1/download/build/day/`

Returns the number of downloads shipper has served in the last 24 hours.

 - `https://host/api/v1/download/build/week/`

Returns the number of downloads shipper has served in the last 7 days.

 - `https://host/api/v1/download/build/month/`

Returns the number of downloads shipper has served in the last 31 days.

 - `https://host/api/v1/download/build/all/`

Returns the number of downloads shipper has served, all time.

## shippy

The following endpoints are used by [shippy, a tool to help maintainers upload builds to shipper.](https://github.com/ericswpark/shippy)

 - `https://host/api/v1/system/info/`

Returns the shipper version installed on the server.

 - `https://host/api/v1/maintainers/login/`

Returns an authentication token when the correct username and password is supplied. The `username` and `password` fields must be supplied via REST.

This endpoint will throw a 400 if either the `username` or `password` field is blank and a 404 if the credentials are invalid.

 - `https://host/api/v1/maintainers/token_check/`

Checks if a REST authentication token is still valid and returns the username of the token bearer if it is. The authentication token must be supplied in the REST header.

 - `https://host/api/v1/maintainers/device/chunked_upload/`

Allows you to upload a build object in chunks given the build file and the corresponding checksum. Multiple fields must be supplied via REST. The authentication token must be supplied in the REST header. This endpoint only accepts the initial chunk, and subsequent chunks must be sent using the endpoint below. Please refer to the shippy project for implementation details.

 - `https://host/api/v1/maintainers/device/chunked_upload/<uuid:pk>`

Allows you to upload the rest of the build object by sending subsequent chunks associated with the chunked upload ID. Multiple fields must be supplied via REST. The authentication token must be supplied in the REST header. Please refer to the shippy project for implementation details.

 - `https://host/api/v1/maintainers/build/enabled_status_modify/`

Allows you to enable/disable a build object. The `build_id` and `enable` fields must be supplied via REST. The authentication token must be supplied in the REST header.

Returns a 200 with the enable/disable status if successful.

This endpoint will throw a 400 if one or more of the required fields are missing and a 401 if you are unauthorized to modify builds.

## Updater

 - `https://host/api/v1/updater/los/<slug:codename>/<slug:variant>/`

This fetches all build objects for the device with the specified `codename` and `variant` slug. There are four possible `variant` slugs: `gapps`, `vanilla` (non-GApps), `foss`, and `goapps` (Go Apps).

This endpoint will throw a 404 if the device is not found or if there are no builds for the specified variant and a 400 if the supplied variant name is invalid.

## General

These are general endpoints used to query information on devices and builds.

 - `https://host/api/v1/general/device/all/`

Shows the list of available devices, their associated codenames, and the variants available for download.

 - `https://host/api/v1/general/build/latest/<slug:codename>/<slug:variant>/`

Returns the latest build for the given device codename and variant.

This endpoint will throw a 404 if the specified device does not exist or if no builds exist for the specified variant yet, with respective error messages for each.