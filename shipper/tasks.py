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

                build = Build.objects.get(file_name=file_name)
                build.sha256sum = sha256sum.hexdigest()
                build.processed = True
                build.save()
