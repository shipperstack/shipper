# Translation

To translate shipper into a new language, follow the steps below!

## Adding a new language

1. Add your language to `config/settings.py`:

```
LANGUAGES = [
    ('ko', gettext('Korean')),
    ('en', gettext('English')),
    # Your language entry here
]
```

2. Use `django-admin` to generate message files for your language:

```
django-admin makemessages -l YOUR_LANGUAGE_CODE_HERE --ignore=docs --ignore=venv
```

The `--ignore` parameters are important, because without it Django will happily search through all the dependencies and documentation of shipper and fetch translation strings for them as well. (Documentation strings are translated separately.)

3. Translate the files in `<app>/locale/YOUR_LANGUAGE_CODE_HERE/LC_MESSAGES`, where `<app>` refers to the following apps in the shipper project:

- accounts
- api
- config
- downloads
- shipper

4. Submit a pull request!

## Updating an existing language

If you are trying to update strings of an existing language, follow the steps below:

1. Use `django-admin` to add new strings to the message files for an existing language:

```
django-admin makemessages -l ko --ignore=docs --ignore=venv
```

Optionally, create messages for all languages:

```
django-admin makemessages -a --ignore=docs --ignore=venv
```

2. Translate the updated files.
3. Submit a pull request!

