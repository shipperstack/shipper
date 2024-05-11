from django.db import models


# noinspection SpellCheckingInspection
class MirrorServer(models.Model):
    name = models.TextField(
        max_length=100,
        help_text="Name that describes the server.<br>"
        "Example: SourceForge, Mirror A, etc.",
        blank=False,
    )
    description = models.TextField(
        max_length=100,
        help_text="Description of the server. This is shown to the users on the mirror "
        "page.",
        blank=True,
    )
    hostname = models.TextField(
        max_length=100,
        help_text="Hostname of the server.<br>"
        "Example: frs.sourceforge.net, mirror.example.com, etc.",
        blank=False,
    )
    ssh_host_fingerprint_type = models.TextField(
        max_length=20,
        help_text="SSH host fingerprint type. Get this with <code>ssh-keyscan "
        "hostname</code>.<br>"
        "Example: ssh-rsa, etc.",
        verbose_name="SSH host fingerprint type",
        blank=False,
    )
    ssh_host_fingerprint = models.TextField(
        max_length=1000,
        help_text="SSH host fingerprint. Get this with <code>ssh-keyscan "
        "hostname</code>.",
        verbose_name="SSH host fingerprint",
        blank=False,
    )
    legacy_connection_mode = models.BooleanField(
        help_text="Disables certain SSH key verification algorithms. We recommend "
        "leaving this unchecked unless something goes wrong during the verification "
        "process.",
        default=False,
    )
    ssh_username = models.TextField(
        max_length=50,
        help_text="SSH username to connect with",
        verbose_name="SSH username",
        blank=False,
    )
    ssh_keyfile = models.TextField(
        max_length=100,
        help_text="SSH keyfile to connect with. Note that the SSH keyfiles must be "
        "placed in the ./ssh/ directory defined in the docker-compose file.<br>"
        "Example: ssh_key, id_rsa, etc.",
        verbose_name="SSH keyfile",
        blank=False,
    )
    upload_path = models.TextField(
        max_length=100,
        help_text="Path to upload to on the server.<br>"
        "Example: /home/frs/project/example/R/, /mnt/media/mirror/src/target/R/, etc.",
    )
    download_url_base = models.TextField(
        max_length=100,
        verbose_name="Download URL base",
        blank=True,
        help_text="Base of downloads URL, should a download URL exist.<br>"
        "Example: if full URL to download is "
        "https://sourceforge.net/projects/demo/files/Q/sunfish/"
        "Bliss-v14.2-sunfish-OFFICIAL-gapps-20210425.zip/download, then the base URL "
        "is https://sourceforge.net/projects/demo/files/Q/{}/download",
    )
    enabled = models.BooleanField(
        default=True,
        help_text="Whether this mirror instance is enabled or not. If disabled, builds "
        "will not be mirrored until the mirror instance is enabled again and a "
        "background refresh task runs.",
    )
    downloadable = models.BooleanField(
        default=False,
        help_text="Whether downloads from this mirror instance is possible or not. If "
        "disabled, this mirror will not be shown to users in the mirror list. Make "
        "sure to set the URL base field above if you enable this option!",
    )
    priority = models.IntegerField(
        default=10,
        help_text="Sets the priority of the mirror in the mirror list. Lower values "
        "will be listed first, and higher values will be listed last.<br>"
        "Note: the main server does not have a priority value and will always be "
        "the first in the mirror list.",
    )
    target_versions = models.TextField(
        max_length=100,
        verbose_name="Target versions",
        blank=True,
        help_text="Build versions to mirror to this server. Specify multiple versions "
        "on each line.<br>"
        'Wildcards are supported with the "*" character.<br>'
        "Example: *, v12.*, v12.5, ...",
    )

    def get_download_url(self, build):
        return self.download_url_base.format(build.get_full_path_file_name())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mirror server"
        verbose_name_plural = "mirror servers"
