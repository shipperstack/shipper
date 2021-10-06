# noinspection PyPackageRequirements
from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


auditlog.register(User)
