import hashlib
import os
import pysftp

from celery import shared_task
from config import settings


@shared_task
def backup_build(build):
    # Check if backup is enabled
    if settings.SHIPPER_ENABLE_SF_BACKUP != 1:
        return

    with pysftp.Connection(
            host="frs.sourceforge.net",
            username=settings.SHIPPER_SF_USERNAME,
            private_key=settings.SHIPPER_SF_PRIVATE_KEY,
    ) as sftp:
        sftp.cwd(
            os.path.join(
                '/home/frs/project/',
                settings.SHIPPER_SF_PATH,
                build.device.codename
            )
        )

        if not sftp.exists(build.device.codename):
            sftp.mkdir(build.device.codename)

        sftp.cwd(build.device.codename)

        sftp.put(os.path.join(settings.MEDIA_ROOT, build.zip_file))
        sftp.put(os.path.join(settings.MEDIA_ROOT, build.md5_file))

    build.backed_up = True
    build.save()


@shared_task
def generate_sha256(build):
    sha256sum = hashlib.sha256()
    with open(build.zip_file, 'rb') as destination:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: destination.read(4096), b""):
            sha256sum.update(byte_block)
    build.sha256sum = sha256sum.hexdigest()
    build.save()
