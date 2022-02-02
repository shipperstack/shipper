import datetime

# noinspection PyPackageRequirements
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin

# Device Model
from config import settings


class Device(models.Model):
    name = models.TextField(max_length=100, help_text="Example: 'Nexus 5X', 'Nexus 6P'")
    codename = models.TextField(max_length=20, help_text="Example: 'bullhead', 'angler'")
    manufacturer = models.TextField(max_length=20, help_text="Example: 'LG', 'Huawei'")
    photo = models.URLField(
        help_text="URL to image of device.<br>Preferably grab an image from <a "
                  "href=\"https://www.gsmarena.com\" target=\"_blank\">GSMArena.</a><br>Example: "
                  "'https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg', "
                  "'https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg'",
        blank=True,
    )
    status = models.BooleanField(default=True, help_text="Device is still maintained - uncheck if abandoned")
    maintainers = models.ManyToManyField(
        get_user_model(),
        related_name="devices",
        help_text="Choose the maintainers working on this device. Multiple maintainers can be selected.<br>",
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{} {} ({})".format(self.manufacturer, self.name, self.codename)

    def get_enabled_builds(self):
        return self.builds.filter(enabled=True)

    def has_enabled_hashed_builds(self):
        return self.get_enabled_builds().exclude(sha256sum__exact='').count() > 0

    def has_enabled_hashed_builds_of_variant(self, variant):
        return self.get_enabled_builds().filter(variant=variant).exclude(sha256sum__exact='').count() > 0

    def get_latest_enabled_hashed_build_of_variant(self, variant):
        return self.get_all_enabled_hashed_builds_of_variant(variant=variant)[0]

    def get_all_builds(self):
        return sorted(self.builds.all(), key=lambda p: p.build_date, reverse=True)

    def get_all_enabled_hashed_builds(self):
        return sorted(self.get_enabled_builds().exclude(sha256sum__exact='').all(), key=lambda p: p.build_date,
                      reverse=True)

    def get_all_enabled_hashed_builds_of_variant(self, variant):
        return sorted(self.get_enabled_builds().filter(variant=variant).exclude(sha256sum__exact='').all(),
                      key=lambda p: p.build_date, reverse=True)


# Mirror Server Model
# noinspection SpellCheckingInspection
class MirrorServer(models.Model):
    name = models.TextField(
        max_length=100,
        help_text='Name that describes the server.<br>'
                  'Example: SourceForge, Mirror A, etc.',
        blank=False,
    )
    description = models.TextField(
        max_length=100,
        help_text='Description of the server. This is shown to the users on the mirror page.',
        blank=True,
    )
    hostname = models.TextField(
        max_length=100,
        help_text='Hostname of the server.<br>'
                  'Example: frs.sourceforge.net, mirror.example.com, etc.',
        blank=False,
    )
    ssh_host_fingerprint_type = models.TextField(
        max_length=20,
        help_text='SSH host fingerprint type. Get this with <code>ssh-keyscan hostname</code>.<br>'
                  'Example: ssh-rsa, etc.',
        verbose_name='SSH host fingerprint type',
        blank=False,
    )
    ssh_host_fingerprint = models.TextField(
        max_length=1000,
        help_text='SSH host fingerprint. Get this with <code>ssh-keyscan hostname</code>.',
        verbose_name='SSH host fingerprint',
        blank=False,
    )
    ssh_username = models.TextField(
        max_length=50,
        help_text='SSH username to connect with',
        verbose_name='SSH username',
        blank=False,
    )
    ssh_keyfile = models.TextField(
        max_length=100,
        help_text='SSH keyfile to connect with. Note that the SSH keyfiles must be placed in the ./ssh/ directory '
                  'defined in the docker-compose file.<br>'
                  'Example: ssh_key, id_rsa, etc.',
        verbose_name='SSH keyfile',
        blank=False,
    )
    upload_path = models.TextField(
        max_length=100,
        help_text='Path to upload to on the server.<br>'
                  'Example: /home/frs/project/example/R/, /mnt/media/mirror/src/target/R/, etc.',
    )
    download_url_base = models.TextField(
        max_length=100,
        verbose_name='Download URL base',
        blank=True,
        help_text='Base of downloads URL, should a download URL exist.<br>'
                  'Example: if full URL to download is https://sourceforge.net/projects/demo/files'
                  '/Q/sunfish/Bliss-v14.2-sunfish-OFFICIAL-gapps-20210425.zip/download, then the base URL is '
                  'https://sourceforge.net/projects/demo/files/Q/{}/download',
    )
    enabled = models.BooleanField(
        default=True,
        help_text='Whether this mirror instance is enabled or not. If disabled, builds will not be mirrored until '
                  'the mirror instance is enabled again and a background refresh task runs.',
    )
    downloadable = models.BooleanField(
        default=False,
        help_text='Whether downloads from this mirror instance is possible or not. If disabled, this mirror will not '
                  'be shown to users in the mirror list. Make sure to set the URL base field above if you enable this '
                  'option!',
    )
    priority = models.IntegerField(
        default=10,
        blank=False,
        help_text='Sets the priority of the mirror in the mirror list. Lower values will be listed first, and higher '
                  'values will be listed last.<br>'
                  'Note: the main server does not have a priority value and will always be the first in the mirror '
                  'list.'
    )
    target_versions = models.TextField(
        max_length=100,
        verbose_name='Target versions',
        blank=True,
        help_text='Build versions to mirror to this server.<br>'
                  '* will mirror all versions. Specify multiple versions using the delimiter set in settings.<br>'
                  'For example, if your delimiter setting is -, then you would specify multiple versions like '
                  'VERSION8-VERSION9. <br>'
                  'Warning: this field does not take a version range! For example, VERSION7-VERSION9 will not '
                  'mirror versions 7 through 9. Rather, it will only mirror versions 7 and 9 and leave out '
                  'version 8.<br>'
                  'Example: v12.8, v12.8-v12.9, *, ...',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mirror server"
        verbose_name_plural = "mirror servers"


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
    size = models.BigIntegerField(
        help_text="Size of zip file in bytes<br>Example: 857483855"
    )
    version = models.TextField(
        max_length=20,
        help_text="Example: v12.8"
    )
    sha256sum = models.TextField(
        max_length=64,
        verbose_name='SHA256 hash'
    )
    variant = models.TextField(
        max_length=20,
        help_text="One of the following variants: gapps, vanilla, goapps, foss"
    )
    build_date = models.DateField(
        help_text="Build date"
    )
    mirrored_on = models.ManyToManyField(
        MirrorServer,
        related_name="builds",
        help_text='Servers this build is mirrored on. Do NOT edit manually.<br>'
                  'Incorrectly modifying this field may result in mirror servers showing for a given build, even if '
                  'the build is not mirrored on said mirror server.',
        blank=True,
    )
    enabled = models.BooleanField(
        default=True,
        help_text='Whether this build is enabled or not. Disabled builds will not show up to users, or in the updater '
                  'API until it is enabled again. Disabled builds are still replicated to mirror servers, so a user '
                  'downloading from a mirror server may see the build listed.'
    )
    download_count = models.BigIntegerField(
        default=0,
        help_text='Approximate download count'
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)

    def get_upload_path(self, filename):
        return "{}/{}".format(self.device.codename, filename)

    zip_file = models.FileField(
        upload_to=get_upload_path,
        verbose_name='Zip file',
        unique=True
    )
    md5_file = models.FileField(
        upload_to=get_upload_path,
        verbose_name='MD5 file',
        unique=True
    )

    def get_user_friendly_name(self):
        _, version, _, _, _, _ = self.file_name.split(settings.SHIPPER_FILE_NAME_FORMAT_DELIMITER)
        date = self.build_date.strftime('%Y-%m-%d')
        return "{} - {}".format(version, date)

    def get_user_friendly_variant_name(self):
        if self.variant in settings.SHIPPER_UPLOAD_VARIANTS:
            return settings.SHIPPER_UPLOAD_VARIANTS[self.variant]
        else:
            return self.variant

    def get_human_readable_size(self):
        import humanize
        return humanize.naturalsize(self.size)

    def get_downloadable_mirrors(self):
        return self.mirrored_on.filter(downloadable=True).all().order_by('priority')

    @admin.display(
        description='Processed',
        boolean=True,
    )
    def is_processed(self):
        return self.sha256sum != ''

    def is_mirrored(self):
        if self.mirrored_on.count() == 0:
            return False

        has_mirror = False

        for mirror in list(MirrorServer.objects.filter(enabled=True)):
            # See if already mirrored
            if mirror in self.mirrored_on.all():
                has_mirror = True
                continue

            # Compare target version string
            target_versions = mirror.target_versions
            if target_versions == "":
                continue
            elif target_versions == "*":
                if mirror not in self.mirrored_on.all():
                    return False
                else:
                    has_mirror = True
            else:
                if obj.version in target_versions.split(settings.SHIPPER_FILE_NAME_FORMAT_DELIMITER):
                    if mirror not in self.mirrored_on.all():
                        return False
                    else:
                        has_mirror = True

        return has_mirror

    def __str__(self):
        return self.file_name


# Download statistics
class Statistics(models.Model):
    date = models.DateField(primary_key=True, default=datetime.date.today)
    download_count = models.BigIntegerField(
        default=0,
        help_text='Download count for this date'
    )

    class Meta:
        verbose_name = "statistic"
        verbose_name_plural = "statistics"


# Register all models to audit log
auditlog.register(Device)
auditlog.register(MirrorServer)
auditlog.register(Build, exclude_fields=['download_count'])
