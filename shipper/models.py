from django.db import models
from django.conf import settings


# Device Model
class Device(models.Model):
    name = models.TextField(max_length=20, help_text="Example: 'Nexus 5X', 'Nexus 6P'")
    codename = models.TextField(max_length=20, help_text="Example: 'bullhead', 'angler'")
    manufacturer = models.TextField(max_length=20, help_text="Example: 'LG', 'Huawei'")
    cpu = models.TextField(max_length=20, help_text="Example: 'MSM8992', 'MSM8994'")
    gpu = models.TextField(max_length=20, help_text="Example: 'Adreno 418', 'Adreno 430'")
    memory = models.IntegerField(
        help_text="RAM amount. Set to lowest value if device has multiple SKUs.<br>Example: '2' if device ships with "
                  "2 or 3 GB of RAM"
    )
    storage = models.IntegerField(
        help_text="Storage amount. Set to lowest value if device has multiple SKUs.<br>Example: '32' if device ships "
                  "with 32 or 64 GB of storage"
    )
    photo = models.URLField(
        help_text="URL to image of device.<br>Preferably grab an image from <a "
                  "href=\"https://www.gsmarena.com\">GSMArena.</a>"
    )
    status = models.BooleanField(default=True, help_text="Device is still maintained - uncheck if abandoned")
    maintainers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="devices",
        help_text="Choose the maintainers working on this device. Multiple maintainers can be selected.<br>"
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name + " (" + self.codename + ")"


# Build Model
class Build(models.Model):
    # Basic build information
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    file_name = models.TextField(max_length=500)    # Bliss-v12.9-xxxx-xxxx.zip
    sourceforge_direct_link = models.URLField()     # https://sourceforge.com/xxx.zip
    size = models.IntegerField()                    # (size of file in bytes) 720924381
    type = models.TextField(max_length=20)          # official
    version = models.TextField(max_length=20)       # v12.9
    gapps = models.BooleanField(default=False)      # Does the build include GApps?
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

