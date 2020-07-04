import os
import hashlib
import pysftp


from celery import Celery
from django.conf import settings

from .models import *
from .utils import delete_artifact

app = Celery('tasks', broker='pyampq://localhost')


'''
Process builds for specified device

Iterate through media/<codename>/*
For each build artifact:
 - Check if same build object exists
     - If yes, then stop. Delete the artifact.
     - If no, then continue
 - Generate a SHA256 hash for the Updater app
 - Upload the build and MD5 files to SourceForge and delete build
 - Create a build object and save to the database
 - Set representative build to latest build
'''
@app.task
def process_build(codename):
    for file in os.scandir(os.path.join(settings.MEDIA_ROOT, codename)):
        if file.path.endswith(".zip"):
            file_name, file_extension = os.path.splitext(file.path)
            _, version, codename, type, date = file_name.split('-')

            sha256sum = hashlib.sha256()

            with open(file_name, "rb") as file:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: file.read(4096), b""):
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
                        '/Q/',
                        codename
                    )
                )

                sftp.put(os.path.join(settings.MEDIA_ROOT, file.path))
                sftp.put(os.path.join(settings.MEDIA_ROOT, file.path, '.md5'))

            delete_artifact(codename, file.path)

            build = Build.objects.get(file_name=file_name)
            build.sha256sum = sha256sum
            build.processed = True
