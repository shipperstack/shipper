SENTRY_SDK_URL = (
    "https://0da75bab4671455ea1b7580cb93649f5@o444286.ingest.sentry.io" "/5645833"
)

NO_CONFIGURATION_WARNING_MSG = """\
No configuration file found or configuration is invalid. You need to configure shippy
before you can start using it.
"""

PRERELEASE_WARNING_MSG = """\
You're running a prerelease build of shippy. Be careful as prerelease versions can
behave in unexpected ways! If you haven't been instructed to test shippy, please
consider switching back to a stable build.
"""

SERVER_COMPAT_ERROR_MSG = """\
The server you're connecting to is out-of-date.
If you know the server admin, please ask them to upgrade the server.
 * Reported server version: \t{}
 * Compatible version: \t\t{}

To prevent data corruption, shippy will not work with an outdated server. Exiting...
"""

SHIPPY_COMPAT_ERROR_MSG = """\
Error: shippy is out-of-date and will not with this server instance.
Upgrade shippy with the following command:
\tpip3 install --upgrade shipper-shippy

Version information:
 * Reported compatible version by server: \t{}
 * Your current shippy version: \t\t{}
"""

SHIPPY_OUTDATED_MSG = """\
Warning: shippy is out-of-date.
 * Current version: \t{}
 * New version: \t{}

We recommend updating shippy with the following command:
\tpip3 install --upgrade shipper-shippy
"""

FOUND_PREVIOUS_BUILD_ATTEMPT_MSG = """\
Found a previous upload attempt for the build {}, created on {}
"""

RATE_LIMIT_MSG = "shippy has been rate limited."
RATE_LIMIT_WAIT_STATUS_MSG = (
    "Waiting to resume after being rate limited. shippy will "
    "resume uploading in {} seconds."
)

WAITING_FINALIZATION_MSG = (
    "Waiting for the server to process the uploaded build. "
    "This may take around 30 seconds..."
)

CANNOT_CONTACT_SERVER_ERROR_MSG = "Cannot contact the server. "
UNEXPECTED_SERVER_RESPONSE_ERROR_MSG = "The server returned an unexpected response. "
FAILED_TO_RETRIEVE_SERVER_VERSION_ERROR_MSG = (
    "Failed to retrieve server version information! "
)
FAILED_TO_LOG_IN_ERROR_MSG = "Failed to log into server! "
UNKNOWN_UPLOAD_START_ERROR_MSG = "Something went wrong starting the upload."
UNKNOWN_UPLOAD_ERROR_MSG = "Something went wrong during the upload."
INTERNAL_SERVER_ERROR_MSG = (
    "An internal server error occurred. Please contact the admins."
)
DISABLE_BUILD_FAILED_MSG = "There was a problem disabling the build."

UNHANDLED_EXCEPTION_MSG = """\
shippy crashed for an unknown reason. :(
To figure out what went wrong, please pass along the full output.
----
URL of request: {}
Request response code: {}
Request response: {}
---
"""

# Chunk size MUST be at 1 MB, as nginx defaults limit request size to that (or less)
CHUNK_SIZE = 1000000
