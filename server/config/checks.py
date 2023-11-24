import os

from django.core.checks import Error, register


@register()
def configuration_check(app_configs, **kwargs):
    errors = []
    checked_keys = [
        ("SHIPPER_SECRET_KEY", "secret key"),
        ("SHIPPER_ALLOWED_HOSTS", "allowed hosts"),
        ("SHIPPER_CSRF_TRUSTED_ORIGINS", "CSRF trusted origins"),
    ]
    for checked_key in checked_keys:
        if os.environ.get(checked_key[0]) is None:
            errors.append(
                Error(
                    f"The {checked_key[1]} setting is not properly configured!",
                    hint="Are you sure you set the environment variables? Make sure "
                    f"{checked_key[0]} is set.",
                    id="config.E001",
                )
            )
    return errors
