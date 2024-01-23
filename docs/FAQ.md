# FAQ


## Q: The download counter is wrong!

Or:
- The download count seems too low/high.
- Some requests don't increase the download counter.

This is a known limitation with shipper. shipper counts downloads in the following scenarios:

1. When the user downloads through the webUI

For downloads to be counted, the user must download through the webUI and click on the green "Download" button. In the background, a script sends a ping to the server with the build information so that it is reflected in the statistics.

If the user has Javascript disabled, then the download will not be counted.

2. When a 3rd party app requests the build info through the API, and then manually pings the server through the API

Apps, such as the OTA updater app, can increase the download count by pinging an API provided by shipper when downloading a particular build. The build information must be supplied through the API.

If the app requests the build information via the API, but does _not_ ping the API upon download start, then the download will not be counted.

Some examples where the download won't be counted:
- User has Javascript disabled and downloads through the webUI
- 3rd party app fetches build info through the API but doesn't notify the server when beginning a download
- User directly navigates to the internal download URL and/or the mirror URL
