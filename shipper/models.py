from django.db import models
from django.conf import settings


# Device Model
class Device(models.Model):
    name = models.TextField()                       # Nexus 5X
    codename = models.TextField(max_length=50)      # bullhead
    manufacturer = models.TextField(max_length=20)  # LG
    maintainers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="devices")


# Variant Model
class Variant(models.Model):
    device = models.ForeignKey(Device)
    name = models.TextField()                       # gapps, no-gapps, etc.


# Build Model
class Build(models.Model):
    variant = models.ForeignKey(Variant)
    file_name = models.TextField(max_length=500)    # Bliss-v12.9-xxxx-xxxx.zip
    sourceforge_direct_link = models.URLField()     # https://sourceforge.com/xxx.zip
    size = models.IntegerField()                    # (size of file in bytes) 720924381
    type = models.TextField(max_length=20)          # official
    version = models.TextField(max_length=20)       # v12.9
    # release = models.TextChoices()    # this needs more work
    created = models.DateTimeField(auto_now_add=True, editable=False)


