import os

import humanize
from constance import config
from django.apps import apps
from django.contrib import admin
from django.db import models
from django.urls import reverse
from datetime import date

from django.utils.translation import get_language

from core.utils import is_version_in_target_versions

LOCALE_MAPPING = {"en": "en_US", "ko": "ko_KR"}


class Build(models.Model):
    # Basic build information
    device = models.ForeignKey(
        "Device",
        related_name="builds",
        on_delete=models.CASCADE,
    )
    file_name = models.TextField(
        max_length=500,
        unique=True,
        help_text="Example: 'Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
    )
    size = models.BigIntegerField(
        help_text="Size of zip file in bytes<br>Example: 857483855"
    )
    version = models.TextField(max_length=20, help_text="Example: v12.8")
    md5sum = models.TextField(max_length=32, verbose_name="MD5 hash")
    sha256sum = models.TextField(max_length=64, verbose_name="SHA256 hash")
    variant = models.ForeignKey("Variant", on_delete=models.PROTECT)
    build_date = models.DateField(help_text="Build date")
    features = models.ManyToManyField(
        "BuildFeature",
        related_name="builds",
        blank=True,
        help_text="Features of this build.",
    )
    mirrored_on = models.ManyToManyField(
        "MirrorServer",
        related_name="builds",
        help_text="Servers this build is mirrored on. Do NOT edit manually.<br>"
        "Incorrectly modifying this field may result in mirror servers showing for a "
        "given build, even if the build is not mirrored on said mirror server.",
        blank=True,
    )
    enabled = models.BooleanField(
        default=True,
        help_text="Whether this build is enabled or not. Disabled builds will not show "
        "up to users, or in the updater API until it is enabled again. Disabled builds "
        "are still replicated to mirror servers, so a user downloading from a mirror "
        "server may see the build listed.",
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)

    def get_upload_path(self, filename):
        return "{}/{}".format(self.device.codename, filename)

    zip_file = models.FileField(
        upload_to=get_upload_path, verbose_name="Zip file", blank=True
    )

    x86_type = models.ForeignKey(
        "X86Type", on_delete=models.PROTECT, blank=True, null=True
    )

    def get_user_friendly_name(self):
        return "{} - {}".format(self.version, self.build_date.strftime("%Y-%m-%d"))

    def get_iso8601_build_date(self):
        return self.build_date.strftime("%Y-%m-%d")

    def get_user_friendly_variant_name(self):
        return self.variant.description

    def get_human_readable_size(self):
        return humanize.naturalsize(self.size)

    def get_downloadable_mirrors(self):
        return self.mirrored_on.filter(downloadable=True).all().order_by("priority")

    def get_download_count(self):
        return self.build_stats.count()

    @admin.display(
        description="Hashed",
        boolean=True,
    )
    def is_hashed(self):
        return self.sha256sum not in ["", None] and self.md5sum not in ["", None]

    @admin.display(
        description="Mirrored",
        boolean=True,
    )
    def is_mirrored(self):
        """
        Checks if the build has been mirrored to mirror servers.
        Criteria:
        - The build must have at least one mirror server to be considered mirrored
        - The build must be mirrored to all mirror servers that target the build version
        - If the build satisfies all of the above, then it is considered mirrored
        :return: Whether the given build is mirrored following the criteria above
        """
        if self.mirrored_on.count() == 0:
            return False

        has_mirror = False
        mirror_server_model = apps.get_model("core", "MirrorServer")

        for mirror in list(mirror_server_model.objects.filter(enabled=True)):
            # See if already mirrored
            if mirror in self.mirrored_on.all():
                has_mirror = True
                continue

            # Compare target version string
            if is_version_in_target_versions(self.version, mirror.target_versions):
                if mirror not in self.mirrored_on.all():
                    return False
                else:
                    has_mirror = True

        return has_mirror

    @admin.display(
        description="Archived",
        boolean=True,
    )
    def is_archived(self):
        age = (date.today() - self.build_date).days
        return age > config.SHIPPER_BUILD_ARCHIVE_DAYS

    def __str__(self):
        return self.file_name

    def get_absolute_url(self):
        return reverse(
            "downloads_build", kwargs={"codename": self.device.codename, "pk": self.id}
        )

    def human_readable_timedelta(self):
        locale = LOCALE_MAPPING[get_language()]
        if locale != "en_US":
            try:
                humanize.i18n.activate(locale=locale)
            except FileNotFoundError:
                pass
        else:
            humanize.i18n.deactivate()
        return humanize.naturaltime(date.today() - self.build_date)

    def zip_file_basename(self):
        return os.path.basename(self.zip_file.name)

    def get_full_path_file_name(self):
        return self.get_upload_path(f"{self.file_name}.zip")

    def is_downloadable_from_main(self):
        return (
            bool(self.zip_file)
            and self.zip_file.storage.exists(self.zip_file.name)
            and not config.SHIPPER_DOWNLOADS_DISABLE_MAIN_SERVER
        )
