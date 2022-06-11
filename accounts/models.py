from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_access_to_devices = models.BooleanField(default=False, help_text="Has access to all devices on shipper")


auditlog.register(User)
