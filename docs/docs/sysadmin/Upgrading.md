# Upgrading

Before upgrading, check out the version-specific changes below first and make any modifications if necessary!

## Automatic

Run the `update-shipper.sh` script located at the root of the repository. Note that the script is not self-updating and should be updated manually, either via git or curl.

If you want to execute the latest version of the `update-shipper.sh` script every time, use the following alias:

```
alias update-shipper='bash < (curl -s https://raw.githubusercontent.com/ericswpark/shipper/master/update-shipper.sh)'
```

## Version specific changes

If you are on release version ______ and would like to upgrade...

### ≤ 1.13.6

The `SHIPPER_FILE_NAME_FORMAT_DELIMITER` configuration key has been removed.

The following new keys have been added:

- `SHIPPER_FILE_NAME_FORMAT`
- `SHIPPER_SECURE_HSTS_SECONDS`
- `SHIPPER_SECURE_SSL_REDIRECT`

Please [refer to the wiki for more information][configuration].

### ≤ 1.13.1

Changed the format of the configuration key `SHIPPER_ADMIN_EMAILS`: now it requires you to specify the admin name as well.

Please [refer to the wiki for more information][configuration].

### ≤ 1.12.0

Several new configuration keys have been added:

- `SHIPPER_FILE_NAME_FORMAT_DELIMITER`
- `SHIPPER_ADMIN_EMAILS`

Please [refer to the wiki for more information][configuration].

### ≤ 1.10.3

The `SHIPPER_UPLOAD_VARIANTS` key has been changed to accept a JSON of variants and user-friendly variant names. In addition, the `SHIPPER_MAIN_WEBSITE_URL` default has been changed, and the default value will prevent the button from showing.

Please [refer to the wiki for more information][configuration].

### ≤ 1.9.16

A key to configure the variants shipper accepts when uploading builds (`SHIPPER_UPLOAD_VARIANTS`) has been added.

Please [refer to the wiki for more information][configuration].

### ≤ 1.9.9

Two new security keys have been added to the configuration, `SHIPPER_CSRF_COOKIE_SECURE` and `SHIPPER_SESSION_COOKIE_SECURE`. Please set them to 0 for development and 1 for production. If you forget to set them, they will default to 1, which is great for production but not for development (unless you have HTTPS set up).

Please [refer to the wiki for more information][configuration].

### ≤ 1.9.3

The `docker-compose.yml` file has been updated as the tag names no longer start with `release-` (example: `ericswpark/shipper:release-1.9.3`)

New releases will only have the tag name appended (example: `ericswpark/shipper:1.9.4`)

### ≤ 1.9.0

shipper now has more configuration keys regarding email. You need to add the following keys:

 - `SHIPPER_EMAIL_BACKEND`
 - `SHIPPER_EMAIL_HOST`
 - `SHIPPER_EMAIL_PORT`
 - `SHIPPER_EMAIL_HOST_USER`
 - `SHIPPER_EMAIL_HOST_PASSWORD`
 - `SHIPPER_EMAIL_USE_TLS`
 - `SHIPPER_DEFAULT_FROM_EMAIL`

Please [refer to the wiki for more information][configuration].

### ≤ 1.8.2

IMPORTANT: Read this in full before starting to upgrade or you may potentially have to start from scratch!

Please perform a backup before attempting an upgrade.

Starting from 1.9.0 shipper uses a custom user model. However, due to Django's limitations, the migrations involved are extremely messy and not standardized.

To solve this problem, release 1.8.3 is a go-between release that creates a "fake" migration for admins to migrate previous systems to. After release 1.8.3, the "fake" migration is modified so that it appears as though the custom user model has existed all along. Then, admins can safely upgrade to 1.9.0 or above, since Django will think the "fake" migration has already been applied and will not re-apply the migration. For new systems, the patched "fake" migration will contain the migration information for the custom user model, so it will work seamlessly without having to throw away previous migrations.

The downside to this approach is that all systems that were previously on 1.8.2 or below MUST upgrade to 1.8.3 first AND perform a database migration. Then the systems can be updated to any later version.

TL;DR - if you are on version 1.8.2 or below:

1. Upgrade to version 1.8.3
2. Perform a database migration with `./manage.py migrate`
3. Upgrade to version 1.9.0 or higher (doesn't matter if you skip over versions for this step, as long as you have migrated on 1.8.3 at least once)


### ≤ 1.6.9

Remove all internal API keys from your environment file. The internal API has been removed. You won't be able to use the internal API anymore in other applications if you upgrade to 1.6.10.

### ≤ 1.6.8

Remove all SourceForge-related keys from your environment file. From now on, all mirror servers should be defined on the admin panel of shipper.

### ≤ 1.6.4

Please create a `.htpasswd` file in the `nginx/` configuration directory using this command:

```
htpasswd -c .htpasswd admin # or any username you want
```

### ≤ 1.6.3

`docker-compose` now expects an environment variable to be set in order to pull the correct image. Run the following:

    export VERSION_TAG=1.6.4 # or whatever version that is latest at the time

Before running any `docker-compose` commands.

### ≤ 1.6.2

 - Remove the `DATABASE` environment variable from `.env`.
 - All environment variables related to shipper now have the `SHIPPER_` prefix.
 - To set up the SourceForge backup, add your SSH key and the associated configuration keys.
 - shipper now uses Ubuntu 20.04 as the base. Therefore, all calls to `python` through `docker-compose` should be changed to `python3`. Example:

```
docker-compose exec web python manage.py migrate --noinput # should be changed from
docker-compose exec web python3 manage.py migrate --noinput # should be changed to
```

Please [refer to the wiki for more information][configuration].

### ≤ 1.4.4

 - When upgrading, all old build objects will have the variant set to "unknown." Please change this manually according to each file name. Valid values are "gapps," "vanilla," "foss," and "goapps."

### ≤ 1.2.3

 - Rename `.env.prod` to `.env` and `.env.prod.db` to `.env.db`.
 - If any of your deployment scripts uses the flags `-f docker-compose.prod.yml --build`, remove these two flags. They are no longer necessary.


[configuration]: Configuration.md