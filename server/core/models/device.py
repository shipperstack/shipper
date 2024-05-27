from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Device(models.Model):
    name = models.TextField(max_length=100, help_text="Example: 'Nexus 5X', 'Nexus 6P'")
    codename = models.TextField(
        max_length=20, help_text="Example: 'bullhead', 'angler'", unique=True
    )
    manufacturer = models.TextField(max_length=20, help_text="Example: 'LG', 'Huawei'")

    # Photo-related fields
    photo_url = models.URLField(
        help_text="URL to image of device.<br>Preferably grab an image from <a "
        'href="https://www.gsmarena.com" target="_blank">GSMArena.</a><br>Example: '
        "'https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg', "
        "'https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg'",
        blank=True,
    )

    def get_image_upload_path(self, filename):
        return f"images/device/{self.codename}/{filename}"

    photo = models.FileField(
        help_text="Photo file of device. If blank, the server will try and download "
        "the photo in the `photo_url` field.",
        blank=True,
        upload_to=get_image_upload_path,
    )
    photo_thumbhash = models.TextField(
        help_text="Thumbhash of device photo. If blank, the server will try and "
        "regenerate it from the photo in the `photo` field.",
        blank=True,
    )

    status = models.BooleanField(
        default=True, help_text="Device is still maintained - uncheck if abandoned"
    )
    maintainers = models.ManyToManyField(
        get_user_model(),
        related_name="devices",
        help_text="Choose the maintainers working on this device. Multiple maintainers "
        "can be selected.<br>",
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    visible = models.BooleanField(
        default=True, help_text="Show device on the main downloads page"
    )

    note = models.TextField(
        help_text="Notes pertaining to device",
        max_length=500,
        blank=True,
    )

    def __str__(self):
        return "{} {} ({})".format(self.manufacturer, self.name, self.codename)

    def get_enabled_builds(self):
        return self.builds.filter(enabled=True)

    def has_enabled_hashed_builds(self):
        return len(self.get_all_enabled_hashed_builds()) > 0

    def has_enabled_hashed_builds_of_variant(self, variant):
        return len(self.get_all_enabled_hashed_builds_of_variant(variant)) > 0

    def get_latest_enabled_hashed_build_of_variant(self, variant):
        if not self.has_enabled_hashed_builds_of_variant(variant=variant):
            raise self.DoesNotExist
        return self.get_all_enabled_hashed_builds_of_variant(variant_codename=variant)[
            0
        ]

    def get_latest_enabled_hashed_build(self):
        if not self.has_enabled_hashed_builds():
            raise self.DoesNotExist
        return self.get_all_enabled_hashed_builds()[0]

    def get_all_builds(self):
        return sorted(self.builds.all(), key=lambda p: p.build_date, reverse=True)

    def get_all_enabled_hashed_builds(self):
        enabled_hashed_build_ids = [
            build.id for build in self.get_enabled_builds() if build.is_hashed()
        ]
        return sorted(
            self.get_enabled_builds().filter(id__in=enabled_hashed_build_ids).all(),
            key=lambda p: p.build_date,
            reverse=True,
        )

    def get_all_enabled_hashed_builds_of_variant(self, variant_codename):
        enabled_hashed_build_ids = [
            build.id for build in self.get_enabled_builds() if build.is_hashed()
        ]
        return sorted(
            self.get_enabled_builds()
            .filter(variant__codename=variant_codename)
            .filter(id__in=enabled_hashed_build_ids)
            .all(),
            key=lambda p: p.build_date,
            reverse=True,
        )

    def get_all_enabled_hashed_builds_of_type_and_variant(
        self, type_codename, variant_codename
    ):
        enabled_hashed_build_ids = [
            build.id for build in self.get_enabled_builds() if build.is_hashed()
        ]
        return sorted(
            self.get_enabled_builds()
            .filter(x86_type__codename=type_codename)
            .filter(variant__codename=variant_codename)
            .filter(id__in=enabled_hashed_build_ids)
            .all(),
            key=lambda p: p.build_date,
            reverse=True,
        )

    def get_absolute_url(self):
        return reverse("downloads_device", kwargs={"codename": self.codename})

    def human_readable_last_updated(self):
        return self.get_latest_enabled_hashed_build().human_readable_timedelta()


# Register all models to audit log
auditlog.register(Device)
