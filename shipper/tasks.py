from __future__ import absolute_import, unicode_literals

import os
import hashlib
import pysftp

from celery import shared_task
from config import settings

from shipper import models
from .utils import delete_artifact


@shared_task
def process_build(codename):
    for file in os.scandir(os.path.join(settings.MEDIA_ROOT, codename)):
        if file.path.endswith(".zip"):
            file_name, file_extension = os.path.splitext(file.path)
            _, version, codename, type, date = file_name.split('-')

            sha256sum = hashlib.sha256()

            with open(file.path, "rb") as file_reader:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: file_reader.read(4096), b""):
                    sha256sum.update(byte_block)

            with pysftp.Connection(
                    host=settings.SOURCEFORGE_SFTP_URL,
                    username=settings.SOURCEFORGE_USERNAME,
                    private_key=settings.SOURCEFORGE_SSH_PRIVATE_KEY
            ) as sftp:
                # Established connection
                sftp.cwd(
                    os.path.join(
                        '/home/frs/project/',
                        settings.SOURCEFORGE_PROJECT,
                        'Q'
                    )
                )

                # Check if directory exists
                if not sftp.exists(codename):
                    sftp.mkdir(codename)

                sftp.cwd(codename)

                sftp.put(os.path.join(settings.MEDIA_ROOT, codename, file.path))
                sftp.put("{}.md5".format(os.path.join(settings.MEDIA_ROOT, codename, file.path)))

            delete_artifact(codename, file.path)

            build = models.Build.objects.get(file_name=file_name)
            build.sha256sum = sha256sum
            build.processed = True

@shared_task
def delete_build(codename, file_name):
    with pysftp.Connection(
            host=settings.SOURCEFORGE_SFTP_URL,
            username=settings.SOURCEFORGE_USERNAME,
            private_key=settings.SOURCEFORGE_SSH_PRIVATE_KEY
    ) as sftp:
        # Established connection
        sftp.cwd(
            os.path.join(
                '/home/frs/project/',
                settings.SOURCEFORGE_PROJECT,
                'Q'
            )
        )

        sftp.cwd(codename)

        try:
            sftp.remove("{}.zip".format(file_name))
            sftp.remove("{}.zip.md5".format(file_name))
        except FileNotFoundError:
            # Builds have been deleted already
            pass

        Build.objects.get(file_name=file_name).delete()
