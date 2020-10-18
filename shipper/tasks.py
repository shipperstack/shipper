from __future__ import absolute_import, unicode_literals

import os
import hashlib
import pysftp

from celery import shared_task
from config import settings

from .models import Build
from .utils import delete_artifact


MAX_RETRY_COUNT = 3


@shared_task
def process_build(codename):
    for file in os.scandir(os.path.join(settings.MEDIA_ROOT, codename)):
        if file.path.endswith(".zip"):
            absolute_file_name = os.path.basename(file.path)
            file_name, file_extension = os.path.splitext(absolute_file_name)
            _, version, codename, type, gapps_raw, date = file_name.split('-')

            sha256sum = hashlib.sha256()

            with open(file.path, "rb") as file_reader:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: file_reader.read(4096), b""):
                    sha256sum.update(byte_block)

            # Retry up to 3 times if connection or upload fails
            for try_count in list(range(MAX_RETRY_COUNT)):
                upload_success = False
                try:
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
                                'R'
                            )
                        )

                        # Check if directory exists
                        if not sftp.exists(codename):
                            sftp.mkdir(codename)

                        sftp.cwd(codename)

                        def print_progress(transferred, total):
                            print("{} transferred out of {} ({:.2f}%)".format(transferred, total, transferred*100/total))

                        print("Beginning file transfer for {}: {}".format(codename, file_name))
                        sftp.put(
                            os.path.join(settings.MEDIA_ROOT, codename, file.path),
                            callback=lambda x, y: print_progress(x, y),
                            confirm=True,
                        )
                        sftp.put(
                            "{}.md5".format(os.path.join(settings.MEDIA_ROOT, codename, file.path)),
                            callback=lambda x, y: print_progress(x, y),
                            confirm=True,
                        )

                        upload_success = True
                        break
                except Exception as e:
                    print(e)
                    print("An exception occurred. Try {} out of {}".format(try_count + 1, MAX_RETRY_COUNT))
                    continue

            if upload_success:
                delete_artifact(codename, file.path)

                build = Build.objects.get(file_name=file_name)
                build.sha256sum = sha256sum.hexdigest()
                build.processed = True
                build.save()


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

        try:
            sftp.cwd(codename)
            sftp.remove("{}.zip".format(file_name))
            sftp.remove("{}.zip.md5".format(file_name))
        except FileNotFoundError:
            # Builds have been deleted already
            pass

        Build.objects.get(file_name=file_name).delete()
