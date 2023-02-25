from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_access_to_devices = models.BooleanField(
        default=False, help_text="Has access to all devices on shipper"
    )
    profile_picture = models.URLField(
        help_text="URL to profile picture.",
        blank=True,
    )
    bio = models.TextField(
        max_length=500,
        help_text="Short bio about yourself!",
        blank=True,
    )
    contact_url = models.URLField(
        help_text="Where users should contact you.<br>Example: https://t.me/@example, "
        "mailto:john.appleseed@example.com ",
        blank=True,
    )


auditlog.register(User)
