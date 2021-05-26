from django.conf import settings
from django.db import models


# Device Model
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
        settings.AUTH_USER_MODEL,
        related_name="devices",
        help_text="Choose the maintainers working on this device. Multiple maintainers can be selected.<br>",
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{} {} ({})".format(self.manufacturer, self.name, self.codename)

    def get_photo_url(self):
        if not self.photo:
            # Return a generic image
            return "#"  # TODO: add URL to generic photo here
        else:
            return self.photo

    def has_gapps_builds(self):
        return self.builds.filter(variant="gapps").exclude(sha256sum__exact='').count() > 0

    def has_vanilla_builds(self):
        return self.builds.filter(variant="vanilla").exclude(sha256sum__exact='').count() > 0

    def has_foss_builds(self):
        return self.builds.filter(variant="foss").exclude(sha256sum__exact='').count() > 0

    def has_goapps_builds(self):
        return self.builds.filter(variant="goapps").exclude(sha256sum__exact='').count() > 0

    def has_builds(self):
        return self.builds.exclude(sha256sum__exact='').count() > 0

    def get_latest_gapps_build_object(self):
        return self.builds.filter(variant="gapps").exclude(sha256sum__exact='').latest('id')

    def get_latest_vanilla_build_object(self):
        return self.builds.filter(variant="vanilla").exclude(sha256sum__exact='').latest('id')

    def get_latest_foss_build_object(self):
        return self.builds.filter(variant="foss").exclude(sha256sum__exact='').latest('id')

    def get_latest_goapps_build_object(self):
        return self.builds.filter(variant="goapps").exclude(sha256sum__exact='').latest('id')

    def get_all_build_objects(self):
        return self.builds.exclude(sha256sum__exact='').all()

    def get_all_gapps_build_objects(self):
        return self.builds.filter(variant="gapps").exclude(sha256sum__exact='').all().order_by('created')

    def get_all_vanilla_build_objects(self):
        return self.builds.filter(variant="vanilla").exclude(sha256sum__exact='').all().order_by('created')

    def get_all_foss_build_objects(self):
        return self.builds.filter(variant="foss").exclude(sha256sum__exact='').all().order_by('created')

    def get_all_goapps_build_objects(self):
        return self.builds.filter(variant="goapps").exclude(sha256sum__exact='').all().order_by('created')


# Mirror Server Model
class MirrorServer(models.Model):
    name = models.TextField(
        max_length=100,
        help_text='Name that describes the server.<br>'
                  'Example: SourceForge, Mirror A, etc.',
        blank=False,
    )
    hostname = models.TextField(
        max_length=100,
        help_text='Hostname of the server.<br>'
                  'Example: frs.sourceforge.net, mirror.example.com, etc.',
        blank=False,
    )
    ssh_host_key_type = models.TextField(
        max_length=20,
        help_text='SSH host key type.<br>'
                  'Example: ssh-rsa, etc.',
        verbose_name='SSH host key type',
        blank=False,
    )
    ssh_host_key = models.TextField(
        max_length=1000,
        help_text='SSH host key.',
        verbose_name='SSH host key',
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
                  'Example: /home/frs/project/example/R/, /mnt/media/mirror/src/target/R/, etc.'
    )
    enabled = models.BooleanField(
        default=True,
        help_text='Whether this mirror instance is enabled or not. If disabled, builds will not be mirrored until '
                  'the mirror instance is enabled again and a background refresh task runs.'
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
    size = models.IntegerField(
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
    mirrored_on = models.ManyToManyField(
        MirrorServer,
        related_name="builds",
        help_text="Servers this build is mirrored on. Do not edit manually unless you know what you are doing!<br>",
        blank=True,
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
        from datetime import datetime
        _, version, _, _, _, date = self.file_name.split('-')
        date = datetime.strptime(date, '%Y%m%d').strftime('%B %-d, %Y')
        return "{} - {}".format(version, date)

    def get_human_readable_size(self):
        import humanize
        return humanize.naturalsize(self.size)

    def __str__(self):
        return self.file_name
