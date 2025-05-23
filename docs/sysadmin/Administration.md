# Administration

## Commands

### shipper

#### `finalize_build_hashes`

Calculates build hashes for builds that do not have them (maybe interrupted mid-upload)

#### `mirror_builds`

Mirrors builds that have not been mirrored yet to the appropriate mirror servers

#### `init_full_user` <`username`>

Initializes a "full" user that has access to all enabled devices. The specified user must exist within shipper first!

#### `deinit_full_user` <`username`>

De-initializes a "full" user by removing access to all enabled devices. The specified user must exist within shipper first!


### `django-dbbackup`

For a full overview on all of the commands, [visit the `django-dbbackup` documentation.][django-dbbackup-docs]

[django-dbbackup-docs]: https://django-dbbackup.readthedocs.io/en/stable/commands.html

#### `dbbackup`

Backs up the database.

#### `dbrestore`

Restores the latest backup of the database.

#### `mediabackup`

Backs up all the media files.

#### `mediarestore`

Restores the latest backup of the media files.

#### `listbackups`

Lists all available backups.


### `drf-chunked-upload`

For details on the command below, [visit the `drf-chunked-upload` source.][drf-chunked-upload-source]

[drf-chunked-upload-source]: https://github.com/jkeifer/drf-chunked-upload/blob/main/src/drf_chunked_upload/management/commands/delete_expired_uploads.py

#### `delete_expired_uploads`

Deletes expired uploads. Use `-i` for interactive.

Do NOT use `-k` as it will delete the file but keep the record on the database. shipper will get confused since the offset is preserved and the upload attempt will fail.
