import hashlib
import os

import paramiko
import pysftp
from celery import shared_task
from paramiko.py3compat import decodebytes

from config import settings
from shipper.models import Build


@shared_task
def backup_build(build_id):
    build = Build.objects.get(id=build_id)

    # Check if backup is enabled
    if settings.SHIPPER_ENABLE_SF_BACKUP != 1:
        print("SourceForge backups are disabled. Not backing up the build. Exiting...")
        return

    # Check if a previous run has already completed a backup
    if build.backed_up:
        return

    keydata = b"""AAAAB3NzaC1yc2EAAAABIwAAAQEA2uifHZbNexw6cXbyg1JnzDitL5VhYs0E65Hk/tLAPmcmm5GuiGeUoI
/B0eUSNFsbqzwgwrttjnzKMKiGLN5CWVmlN1IXGGAfLYsQwK6wAu7kYFzkqP4jcwc5Jr9UPRpJdYIK733tSEmzab4qc5Oq8izKQKIaxXNe7FgmL15HjSpatF
t9w/ot/CHS78FUAr3j3RwekHCm/jhPeqhlMAgC+jUgNJbFt3DlhDaRMa0NYamVzmX8D47rtmBbEDU3ld6AezWBPUR5Lh7ODOwlfVI58NAf/aYNlmvl2TZiau
BCTa7OPYSyXJnIPbQXg6YQlDknNCr0K769EjeIlAfY87Z4tw=="""
    key = paramiko.RSAKey(data=decodebytes(keydata))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add('frs.sourceforge.net', 'ssh-rsa', key)

    with pysftp.Connection(
            host="frs.sourceforge.net",
            username=settings.SHIPPER_SF_USERNAME,
            private_key=settings.SHIPPER_SF_PRIVATE_KEY,
            cnopts=cnopts
    ) as sftp:
        sftp.cwd(
            os.path.join(
                '/home/frs/project/',
                settings.SHIPPER_SF_PATH,
            )
        )

        if not sftp.exists(build.device.codename):
            sftp.mkdir(build.device.codename)

        sftp.cwd(build.device.codename)

        sftp.put(os.path.join(settings.MEDIA_ROOT, build.zip_file.name))
        sftp.put(os.path.join(settings.MEDIA_ROOT, build.md5_file.name))

    build.backed_up = True
    build.save()


@shared_task
def generate_sha256(build_id):
    build = Build.objects.get(id=build_id)

    # Check if this task has already been run
    if build.sha256sum != '':
        return

    sha256sum = hashlib.sha256()
    with open(os.path.join(settings.MEDIA_ROOT, build.zip_file.name), 'rb') as destination:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: destination.read(4096), b""):
            sha256sum.update(byte_block)
    build.sha256sum = sha256sum.hexdigest()
    build.save()
