# Configuration

To configure shipper, you need to copy the environment variable files and tweak the values inside.

## `.env`

Copy the `.env.example` file and set the values:

### Django internal
  - `SHIPPER_SECRET_KEY`
    - Django's secret key value, used internally for encryption, etc.
    - [Generate a random key](https://humberto.io/blog/tldr-generate-django-secret-key/) if you are starting a new shipper instance.
    - Required, no defaults provided.
  - `SHIPPER_DEBUG`:
    - Django's debug mode
    - `0` -> disabled (recommended for production)
    - `1` -> enabled (recommended for development)
    - Default: `0`
  - `SHIPPER_ALLOWED_HOSTS`
    - An array of allowed hosts in String format, with spaces delimiting each entry.
    - Example: if you're serving shipper at https://downloads.example.com, you would put `downloads.example.com` here.
    - Required, no defaults provided.
  - `SHIPPER_CSRF_TRUSTED_ORIGINS`
    - An array of trusted origins for CSRF in String format, with spaces delimiting each entry.
    - Should be similar to the `SHIPPER_ALLOWED_HOSTS` config key above, but **must** include the scheme (HTTP or HTTPS)
    - Example: if you're serving shipper at https://downloads.example.com, you would put `https://downloads.example.com` here.
    - Required, no defaults provided
  - `SHIPPER_CSRF_COOKIE_SECURE`
    - Internal Django security option.
    - `1` -> enabled (recommended for production)
    - `0` -> disabled
    - Default: `1`
  - `SHIPPER_SESSION_COOKIE_SECURE`
    - Internal Django security option.
    - `1` -> enabled (recommended for production)
    - `0` -> disabled
    - Default: `1`
  - `SHIPPER_SECURE_HSTS_SECONDS`
    - Internal Django security option to set up HSTS, a mechanism to only allow HTTPS traffic
    - `0` -> HSTS is disabled
    - Setting this key to any value other than 0 will enable HSTS for the specified duration (in seconds)
    - Warning: make sure you know what you are doing! Improper settings may block you from accessing your instance.
    - Default: `0`

### Upload
  - `SHIPPER_UPLOAD_CHECKSUM`
    - Checksum type shipper expects when uploading via the chunked upload API
    - Supports the following options:
      - `md5`
      - `sha256`
    - Default: `sha256`

### Database
  - `SHIPPER_SQL_ENGINE`
    - Database type. Currently only supports the following options:
    - `django.db.backends.postgresql` -> PostgreSQL
    - Not specified -> SQLite
    - Default: SQLite
  - `SHIPPER_SQL_DATABASE`
    - Database name
    - Not specified -> SQLite
    - Default: SQLite
  - `SHIPPER_SQL_USER`
    - Database username
    - Default: `user`
  - `SHIPPER_SQL_PASSWORD`
    - Database password
    - Default: `password`
    - Warning: do NOT leave this variable unchanged in production!
  - `SHIPPER_SQL_HOST`
    - Database host
    - Default: `localhost`
  - `SHIPPER_SQL_PORT`
    - Database port
    - Default: `5432`

### Email
  - `SHIPPER_EMAIL_BACKEND`:
    - `django.core.mail.backends.console.EmailBackend` -> Local email (dummy option for debug use only!)
    - `django.core.mail.backends.smtp.EmailBackend` -> SMTP-based email (recommended for production!)
    - Default: `django.core.mail.backends.console.EmailBackend`
    - Warning: if set to `django.core.mail.backends.console.EmailBackend`, most of the keys below related to email will be ignored.
  - `SHIPPER_EMAIL_HOST`
    - Email (SMTP) host
    - Required if `SHIPPER_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`
  - `SHIPPER_EMAIL_PORT`
    - Email (SMTP) host port
    - Required if `SHIPPER_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`
  - `SHIPPER_EMAIL_HOST_USER`
    - Email username
    - Required if `SHIPPER_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`
  - `SHIPPER_EMAIL_HOST_PASSWORD`
    - Email password
    - Required if `SHIPPER_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`
  - `SHIPPER_EMAIL_USE_TLS`:
    - `0` -> disabled
    - `1` -> enabled (recommended for production)
    - Default: `1`
  - `SHIPPER_DEFAULT_FROM_EMAIL`
    - "From" field in emails, like "Joe McJoeFace \<joe@example.com\>"
    - Required if `SHIPPER_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`
  - `SHIPPER_ADMIN_EMAILS`
    - A list of admins and their emails, delimited with : and ;
    - Format: `AdminName:adminemail@example.com;Admin2Name:admin2email@example.com`
    - Default: ``, disabled

### Sentry (error reporting):
  - `SHIPPER_SENTRY_SDK_DSN`
    - [Sentry](https://sentry.io) bug tracking
    - Recommended: https://34fd99861ec84ad2bd731c50267dc5f6@o444286.ingest.sentry.io/5418995 -> will help with future development of shipper
    - Default: ``, disabled
  - `SHIPPER_SENTRY_SDK_PII`
    - Send potential personally-identifiable information (PII) to Sentry when submitting bug reports
    - `0` -> disabled
    - Any other value -> enabled
    - Default: `0`
    - Warning: if enabled, shipper may send PII such as usernames and email addresses. Set to `False` in production.

## `.env.db`

Copy the `.env.db.example` file and set the values:

  - `POSTGRES_USER`
    - Postgres user
    - Should match the `SHIPPER_SQL_USER` config key above.
  - `POSTGRES_PASSWORD`
    - Postgres user password
    - Should match the `SHIPPER_SQL_PASSWORD` config key above.
  - `POSTGRES_DB`
    - Postgres database name
    - Should match the `SHIPPER_SQL_DATABASE` config key above.
