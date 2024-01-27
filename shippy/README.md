# shippy

[
![PyPI](https://img.shields.io/pypi/v/shipper-shippy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/shipper-shippy)
](https://pypi.org/project/shipper-shippy/)

Client-side tool to interface with shipper

# Usage

Get shippy from PyPI:

```shell
pip3 install --upgrade shipper-shippy
```

Go to the directory with build files, and run:

```shell
shippy
```

Run `shippy -h` to see commandline arguments' usage instructions.

# Configuration

shippy stores its configuration in `~/.shippy.ini`. An example configuration file is shown below:

```ini
[shippy]
server = https://example.com
token = a1b2c3d4e5...
DisableBuildOnUpload = false
UploadWithoutPrompt = false
debug = false
```

Configuration options explained:

### `server`

Server URL

### `token`

Token used to sign in to the server

### `DisableBuildOnUpload`

Immediately disables the build after uploading it. Useful if you are uploading from Jenkins or uploading potentially
unstable builds. Do NOT use under normal circumstances!

### `UploadWithoutPrompt`

shippy will not prompt you before uploading builds, and will automatically upload all builds found in the current
directory. Use with caution. Same as the `-y`/`--yes` flag shown above.

### `debug`

Enable debug mode for all invocations. When set to true, the `-d`/`--debug` flag will have no effect, and all
invocations of shippy will run with debug mode enabled.
