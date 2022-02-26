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
  - `SHIPPER_SECURE_SSL_REDIRECT`
    - Internal Django security option to enable HTTPS redirects
    - `1` -> enabled, Django automatically redirects HTTP traffic to HTTPS (recommended for production)
    - `0` -> disabled
    - Default: `1`

### Downloads Page
  - `SHIPPER_MAIN_WEBSITE_URL`
    - Link to redirect users to when they click on the "Back to main website" button on the top of the page.
    - Default: `#` (no redirection), button does not show
  - `SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING`
    - Sets the navbar branding at the top left
    - Default: "Downloads"
  - `SHIPPER_DOWNLOADS_PAGE_DONATION_URL`
    - URL to refer users to when they wish to donate
    - Default: `#` (no redirection), banner does not show
  - `SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE`
    - Donation message to show to users in donation banner
    - Default: `Please consider donating, thank you!`, banner showing depends on previous configuration key

### Upload
  - `SHIPPER_UPLOAD_VARIANTS`
    - Allowed upload variant pairing in JSON format
    - Format: `{"variant": "variant_friendly_name", "different_variant": "different_variant_friendly_name", ...}`
    - Default: `{"gapps": "GApps","vanilla": "Vanilla (no GApps)","foss": "FOSS","goapps": "GoApps (Android Go Edition GApps)"}`
  - `SHIPPER_FILE_NAME_FORMAT`
    - Regex pattern to use when parsing file names of uploaded artifacts
    - The pattern must include the following four named match groups in order to be considered valid; otherwise an `ImproperlyConfigured` exception will be raised:
        - `version`
        - `codename`
        - `variant`
        - `date`
    - Format: `[A-Za-z]*-(?P<version>[a-z0-9.]*)-(?P<codename>[A-Za-z]*)-OFFICIAL-(?P<variant>[a-z]*)-(?P<date>[0-9]*).zip`

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
    - Default: `False`
    - Warning: if set to `True`, shipper may send PII such as usernames and email addresses. Set to `False` in production.

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

## Create a password for Flower

Flower is a monitoring tool for Celery workers. It is important that you create an access control password to prevent unauthorized access to the Flower instance.

Run the following within the `nginx/` configuration directory:

```
htpasswd -c .htpasswd admin # or any username you prefer
```

Once you're done configuring shipper, [move to the Installation section to install with Docker](Installation.md)!