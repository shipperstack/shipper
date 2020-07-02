from django.db import models
from django.conf import settings


# Device Model
class Device(models.Model):
    name = models.TextField(max_length=20)          # Nexus 5X
    codename = models.TextField(max_length=20)      # bullhead
    manufacturer = models.TextField(max_length=20)  # LG
    cpu = models.TextField(max_length=20)           # MSM8940
    gpu = models.TextField(max_length=20)           # Adreno 420
    memory = models.IntegerField()                  # 2 (in gigabytes)
    storage = models.IntegerField()                 # 512 (in gigabytes)
    photo = models.URLField()                       # Image of device
    status = models.BooleanField(default=True)      # True - device is still maintained
    maintainers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="devices")
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name + " (" + self.codename + ")"


# Variant Model
class Variant(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.TextField()                       # gapps, no-gapps, etc.
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name + " - " + str(self.device)


# Build Model
class Build(models.Model):
    # Basic build information
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    file_name = models.TextField(max_length=500)    # Bliss-v12.9-xxxx-xxxx.zip
    sourceforge_direct_link = models.URLField()     # https://sourceforge.com/xxx.zip
    size = models.IntegerField()                    # (size of file in bytes) 720924381
    type = models.TextField(max_length=20)          # official
    version = models.TextField(max_length=20)       # v12.9
    created = models.DateTimeField(auto_now_add=True, editable=False)

    # Build Release Types
    STABLE = 'STABLE'
    BETA = 'BETA'
    ALPHA = 'ALPHA'
    RELEASE_CHOICES = [
        (STABLE, 'Stable'),
        (BETA, 'Beta'),
        (ALPHA, 'Alpha'),
    ]
    release = models.TextField(
        max_length=10,
        choices=RELEASE_CHOICES,
        default=STABLE,
    )


