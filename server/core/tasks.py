import hashlib
import json
import os
import tempfile
import time
import requests
import datetime
from contextlib import contextmanager

import paramiko
from billiard.exceptions import TimeLimitExceeded, SoftTimeLimitExceeded
from constance import config
from django.conf import settings
from django.core import files
from django.core.cache import cache
from django.db import transaction
from base64 import decodebytes

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django_celery_results.models import TaskResult
from drf_chunked_upload import settings as drf_settings
from drf_chunked_upload.models import ChunkedUpload
from thumbhash import image_to_thumbhash


from .exceptions import BuildMirrorException
from .models import Build, MirrorServer, Device
from .utils import is_version_in_target_versions


logger = get_task_logger(__name__)


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + settings.CELERY_TASK_TIME_LIMIT - 3
    status = cache.add(lock_id, oid, settings.CELERY_TASK_TIME_LIMIT)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@shared_task(
    name="process_incomplete_builds",
    queue="default",
)
def process_incomplete_builds():
    for build in [build for build in Build.objects.all() if not build.is_hashed()]:
        generate_checksum.delay(build.id)

    for build in [
        build
        for build in Build.objects.all()
        if not build.is_mirrored() and not build.is_archived()
    ]:
        mirror_build.delay(build.id)


@shared_task(
    name="mirror_build",
    bind=True,
    default_retry_delay=60 * 60,
    autoretry_for=(TimeLimitExceeded, SoftTimeLimitExceeded),
    retry_backoff=True,
    concurrency=1,
    queue="mirror_upload",
)
def mirror_build(self, build_id):
    if not config.SHIPPER_ENABLE_MIRRORING:
        return

    try:
        build = Build.objects.get(id=build_id)
    except Build.DoesNotExist:
        logger.warning(f"Build with ID {build_id} no longer exists. Exiting...")
        return

    # Setup lock
    lock_id = "{}-lock-{}".format(self.name, build.id)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            mirrors = MirrorServer.objects.filter(enabled=True)

            if len(mirrors) == 0:
                logger.warning("No mirror servers found to mirror to. Exiting...")
                return

            if build.is_archived():
                logger.warning(
                    f"Build {build.file_name} is an archived build! Not mirroring..."
                )
                return

            for mirror in mirrors:
                # Check if a previous run has already completed a backup
                if mirror in build.mirrored_on.all():
                    continue

                if not is_version_in_target_versions(
                    build.version, mirror.target_versions
                ):
                    continue

                upload_build_to_mirror(self, build_id, build, mirror)
        else:
            logger.warning(
                f"Build {build.file_name} is already being mirrored by another process!"
            )
            return


def upload_build_to_mirror(self, build_id, build, mirror):
    sftp = sftp_client_init(mirror)

    # Check if device directory exists and change into it
    try:
        sftp.stat(build.device.codename)
    except FileNotFoundError:
        sftp.mkdir(build.device.codename)
    sftp.chdir(build.device.codename)

    start_time = datetime.datetime.now()

    # Define callback for printing progress
    def update_progress(current, total):
        current_time = datetime.datetime.now()
        elapsed_time = current_time - start_time

        if current > 0:
            remaining_sec = elapsed_time.total_seconds() * (
                float(total - current) / current
            )
        else:
            remaining_sec = 0

        self.update_state(
            state="PROGRESS",
            meta={
                "current": current,
                "total": total,
                "elapsed": elapsed_time.total_seconds(),
                "remaining": remaining_sec,
            },
        )

    try:
        target_file_name = f"{build.file_name}.zip"
        temp_target_file_name = f"{target_file_name}.part"

        logger.info("Starting upload...")
        try:
            sftp.put(
                localpath=os.path.join(settings.MEDIA_ROOT, build.zip_file.name),
                remotepath=temp_target_file_name,
                callback=update_progress,
            )
        except (OSError, EOFError) as e:
            raise BuildMirrorException(
                {
                    "message": "An error occured while uploading the build "
                    "file.",
                    "exception_message": e,
                }
            )

        try:
            sftp.stat(target_file_name)
            logger.warning(f"Found existing file at {target_file_name}")
            sftp.remove(target_file_name)
        except FileNotFoundError:
            pass

        sftp.rename(temp_target_file_name, target_file_name)
        logger.info("Upload complete!")

        # Fetch build one more time and lock until save completes
        logger.info("Saving the success result to the database...")
        with transaction.atomic():
            build = Build.objects.select_for_update().get(id=build_id)
            build.mirrored_on.add(mirror)
            build.save()
        logger.info("Database successfully updated.")
    except SoftTimeLimitExceeded as e:
        raise BuildMirrorException(
            {
                "message": "This build did not mirror within the time limit.",
                "exception_message": e,
            }
        )


def sftp_client_init(mirror):
    ssh = paramiko.SSHClient()

    # Add host key specified to client
    host_key_raw = str.encode(mirror.ssh_host_fingerprint)
    host_key = paramiko.RSAKey(data=decodebytes(host_key_raw))
    ssh.get_host_keys().add(mirror.hostname, mirror.ssh_host_fingerprint_type, host_key)

    # Get private key
    private_key_path = f"/home/shipper/ssh/{mirror.ssh_keyfile}"
    try:
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    except PermissionError as e:
        raise BuildMirrorException(
            {
                "message": "Cannot access SSH key. Is the permission correct?",
                "exception_message": e,
            }
        )
    except FileNotFoundError as e:
        raise BuildMirrorException(
            {
                "message": "SSH key not found. Make sure that the provided SSH key "
                "exists in the directory.",
                "exception_message": e,
            }
        )

    # Connect client
    try:
        # noinspection SpellCheckingInspection
        if not mirror.legacy_connection_mode:
            ssh.connect(
                hostname=mirror.hostname,
                username=mirror.ssh_username,
                pkey=private_key,
            )
        else:
            ssh.connect(
                hostname=mirror.hostname,
                username=mirror.ssh_username,
                pkey=private_key,
                disabled_algorithms={"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
            )
    except (
        ConnectionError,
        EOFError,
    ) as e:
        raise BuildMirrorException(
            {
                "message": "A temporary error occurred connecting to the mirror "
                "server.",
                "exception_message": e,
            }
        )
    sftp = ssh.open_sftp()
    try:
        sftp.chdir(mirror.upload_path)
    except OSError as e:
        raise BuildMirrorException(
            {
                "message": "Cannot access upload path. Make sure that the upload path "
                "is correct.",
                "exception_message": e,
            }
        )
    return sftp


def update_hash(hash_type, build):
    with open(
        os.path.join(settings.MEDIA_ROOT, build.zip_file.name), "rb"
    ) as destination:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: destination.read(4096), b""):
            hash_type.update(byte_block)


@shared_task(
    name="generate_checksum",
    queue="default",
)
def generate_checksum(build_id):
    build = Build.objects.get(id=build_id)

    # Check if MD5 is already generated
    if build.md5sum not in [None, ""]:
        logger.warning(f"Build {build.file_name}'s MD5 generated by another process!")
    else:
        md5sum = hashlib.md5()
        update_hash(md5sum, build)

        # Lock build and update MD5 hash
        with transaction.atomic():
            Build.objects.select_for_update().filter(id=build_id).update(
                md5sum=md5sum.hexdigest()
            )

    # Check if SHA256 is already generated
    if build.sha256sum not in [None, ""]:
        logger.warning(
            f"Build {build.file_name}'s SHA256 generated by another process!"
        )
    else:
        sha256sum = hashlib.sha256()
        update_hash(sha256sum, build)

        # Lock build and update SHA256 hash
        with transaction.atomic():
            Build.objects.select_for_update().filter(id=build_id).update(
                sha256sum=sha256sum.hexdigest()
            )


@shared_task(
    bind=True,
    default_retry_delay=60 * 60,
    autoretry_for=(TimeLimitExceeded,),
    retry_backoff=True,
    queue="mirror_build",
)
def delete_mirrored_build(self, build_id, mirror_server_id):
    build = Build.objects.get(id=build_id)

    # Setup lock
    lock_id = "{}-lock-{}".format(self.name, build.id)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            mirror = MirrorServer.objects.get(id=mirror_server_id)

            if mirror not in build.mirrored_on.all():
                logger.info(
                    f"Build {build.file_name} is not mirrored on mirror server "
                    f"{mirror.name}!"
                )

            sftp = sftp_client_init(mirror)

            # Check if device directory exists and change into it
            try:
                sftp.stat(build.device.codename)
            except FileNotFoundError:
                logger.error(
                    "The device directory does not exist on the mirror server!"
                )
                return

            # Delete build from server
            sftp.remove(path=f"{build.file_name}.zip")

            # Fetch build one more time and lock until save completes
            with transaction.atomic():
                build = Build.objects.select_for_update().get(id=build_id)
                build.mirrored_on.remove(mirror)
                build.save()
        else:
            logger.warning(
                f"Build {build.file_name} is already being deleted from the mirror "
                f"server by another process!"
            )


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


@shared_task(
    name="mirror_build_async_result_cleanup",
    queue="default",
)
def mirror_build_async_result_cleanup():
    # Get all tasks that are in progress
    in_progress_task_results = TaskResult.objects.filter(status="PROGRESS")

    for task in in_progress_task_results:
        elapsed_time = int((timezone.now() - task.date_created).total_seconds())
        logger.info(f"Elapsed time for task ID {task.id} is {elapsed_time}.")

        # Give the check a 30-second leeway, just in case Celery is still cleaning up
        if elapsed_time + 30 > settings.CELERY_TASK_TIME_LIMIT:
            logger.warning(
                f"Task ID {task.id} is over the time limit. Manually setting as failed."
            )
            task.status = "FAILURE"
            task.save()


@shared_task(
    name="device_photo_download",
    queue="default",
)
def device_photo_download():
    # Get all devices with blank photo fields and populated photo_url fields
    target_devices = Device.objects.filter(photo="").exclude(photo_url__exact="")

    for device in target_devices:
        # Get image
        r = requests.get(device.photo_url, stream=True)

        if r.status_code != requests.codes.ok:
            logger.error(f"Photo download failed for device {device.codename}!")
            continue

        file_name = device.photo_url.split("/")[-1]
        temp = tempfile.NamedTemporaryFile()

        for block in r.iter_content(1024 * 8):
            if not block:
                break

            temp.write(block)

        device.photo.save(file_name, files.File(temp))


@shared_task(
    name="device_photo_thumbhash_generate",
    queue="default",
)
def device_photo_thumbhash_generate():
    # Get all devices with blank photo_thumbhash fields and populated photo fields
    target_devices = Device.objects.filter(photo_thumbhash="").exclude(photo="")

    for device in target_devices:
        # Open image for reading
        with device.photo.open("rb") as photo:
            device.photo_thumbhash = image_to_thumbhash(photo)
            device.save()


@shared_task(
    name="drf_chunked_upload_cleanup",
    queue="default",
)
def drf_chunked_upload_cleanup():
    chunked_uploads = ChunkedUpload.objects.filter(
        created_at__lt=(timezone.now() - drf_settings.EXPIRATION_DELTA)
    )

    for chunked_upload in chunked_uploads:
        chunked_upload.delete()
