# Administration

## Commands

### `finalize_build_hashes`

Calculates build hashes for builds that do not have them (maybe interrupted mid-upload)

### `upload_backups`

Uploads build backups to all enabled mirror servers if the builds have not been backed up before

### `init_full_user` <`username`>

Initializes a "full" user that has access to all enabled devices. The specified user must exist within shipper first!

### `deinit_full_user` <`username`>

De-initializes a "full" user by removing access to all enabled devices. The specified user must exist within shipper first!