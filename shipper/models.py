from django.db import models
from django.conf import settings


# Device Model
class Device(models.Model):
    name = models.TextField(max_length=100, help_text="Example: 'Nexus 5X', 'Nexus 6P'")
    codename = models.TextField(max_length=20, help_text="Example: 'bullhead', 'angler'")
    manufacturer = models.TextField(max_length=20, help_text="Example: 'LG', 'Huawei'")
    cpu = models.TextField(
        name="CPU",
        max_length=20,
        help_text="Example: 'MSM8992', 'MSM8994'",
    )
    gpu = models.TextField(
        name="GPU",
        max_length=20,
        help_text="Example: 'Adreno 418', 'Adreno 430'",
    )
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
                  "href=\"https://www.gsmarena.com\" target=\"_blank\">GSMArena.</a><br>Example: "
                  "'https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg', "
                  "'https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg'"
    )
    status = models.BooleanField(default=True, help_text="Device is still maintained - uncheck if abandoned")
    maintainers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="devices",
        help_text="Choose the maintainers working on this device. Multiple maintainers can be selected.<br>",
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{} {} ({})".format(self.manufacturer, self.name, self.codename)

    def has_gapps_builds(self):
        return self.builds.filter(variant="gapps").count() > 0

    def has_vanilla_builds(self):
        return self.builds.filter(variant="vanilla").count() > 0

    def has_foss_builds(self):
        return self.builds.filter(variant="foss").count() > 0

    def has_goapps_builds(self):
        return self.builds.filter(variant="goapps").count() > 0

    def has_builds(self):
        return self.builds.count() > 0

    def get_latest_gapps_build_object(self):
        return self.builds.filter(variant="gapps").latest('id')

    def get_latest_vanilla_build_object(self):
        return self.builds.filter(variant="vanilla").latest('id')

    def get_latest_foss_build_object(self):
        return self.builds.filter(variant="foss").latest('id')

    def get_latest_goapps_build_object(self):
        return self.builds.filter(variant="goapps").latest('id')

    def get_all_build_objects(self):
        return self.builds.all()

    def get_all_gapps_build_objects(self):
        return self.builds.filter(variant="gapps").all()

    def get_all_vanilla_build_objects(self):
        return self.builds.filter(variant="vanilla").all()

    def get_all_foss_build_objects(self):
        return self.builds.filter(variant="foss").all()

    def get_all_goapps_build_objects(self):
        return self.builds.filter(variant="goapps").all()


# Build Model
class Build(models.Model):
    # Basic build information
    device = models.ForeignKey(
        Device,
        related_name="builds",
        on_delete=models.CASCADE,
    )
    file_name = models.TextField(
        max_length=500,
        unique=True,
        help_text="Example: 'Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
    size = models.IntegerField(
        help_text="Size of zip file in bytes<br>Example: 857483855"
    )
    version = models.TextField(
        max_length=20,
        help_text="Example: v12.8"
    )
    sha256sum = models.TextField(max_length=64)
    variant = models.TextField(
        max_length=20,
        help_text="One of the following variants: gapps, vanilla, goapps, foss"
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)

    def get_upload_path(self, filename):
        return "{}/{}".format(self.device.codename, filename)

    zip_file = models.FileField(upload_to=get_upload_path, unique=True)
    md5_file = models.FileField(upload_to=get_upload_path, unique=True)

    def __str__(self):
        return self.file_name
