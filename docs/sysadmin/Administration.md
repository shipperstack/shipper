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

