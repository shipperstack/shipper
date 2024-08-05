import os
import inspect

import django.contrib.postgres.fields

import django.apps
from django.core.checks import Error, register


# noinspection PyUnusedLocal
@register()
def configuration_check(app_configs, **kwargs):
    errors = []
    checked_keys = [
        ("SHIPPER_SECRET_KEY", "secret key"),
        ("SHIPPER_ALLOWED_HOSTS", "allowed hosts"),
        ("SHIPPER_CSRF_TRUSTED_ORIGINS", "CSRF trusted origins"),
    ]
    for checked_key in checked_keys:
        if (
            os.environ.get(checked_key[0]) is None
            or os.environ.get(checked_key[0]) == ""
        ):
            errors.append(
                Error(
                    f"The {checked_key[1]} setting is not properly configured!",
                    hint="Are you sure you set the environment variables? Make sure "
                    f"{checked_key[0]} is set.",
                    id="config.E001",
                )
            )
    return errors


# noinspection PyUnusedLocal
@register()
def disallow_postgres_specific_fields_check(app_configs, **kwargs):
    errors = []
    disallowed_fields = [
        item[1]
        for item in inspect.getmembers(django.contrib.postgres.fields, inspect.isclass)
    ]

    for model in django.apps.apps.get_models():
        for field in model._meta.get_fields():
            for disallowed_field in disallowed_fields:
                # PyCharm bug, see: https://youtrack.jetbrains.com/issue/PY-32860
                # noinspection PyTypeHints
                if isinstance(field, disallowed_field):
                    errors.append(
                        Error(
                            f"Field {field} cannot be used as it is a Postgres-specific field: "
                            f"{disallowed_field.__name__}",
                            hint="Use fields that are database engine-agnostic and provided by Django.",
                            id="config.E002",
                        )
                    )

    return errors
