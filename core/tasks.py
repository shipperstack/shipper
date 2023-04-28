import hashlib
import json
import os
import time
from contextlib import contextmanager

import paramiko
from billiard.exceptions import TimeLimitExceeded, SoftTimeLimitExceeded
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from base64 import decodebytes

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django_celery_results.models import TaskResult

import config.settings
from .models import Build, MirrorServer
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

    for build in [build for build in Build.objects.all() if not build.is_mirrored()]:
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
    build = Build.objects.get(id=build_id)

    # Setup lock
    lock_id = "{}-lock-{}".format(self.name, build.id)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            mirrors = MirrorServer.objects.filter(enabled=True)

            if len(mirrors) == 0:
                logger.warning("No mirror servers found to mirror to. Exiting...")
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

    # Define callback for printing progress
    def update_progress(transferred, total):
        self.update_state(
            state="PROGRESS",
            meta={"current": transferred, "total": total},
        )

    try:
        logger.info("Starting upload...")
        sftp.put(
            localpath=os.path.join(settings.MEDIA_ROOT, build.zip_file.name),
            remotepath=f"{build.file_name}.zip",
            callback=update_progress,
        )
        logger.info("Upload complete!")

        # Fetch build one more time and lock until save completes
        logger.info("Saving the success result to the database...")
        with transaction.atomic():
            build = Build.objects.select_for_update().get(id=build_id)
            build.mirrored_on.add(mirror)
            build.save()
        logger.info("Database successfully updated.")
    except SoftTimeLimitExceeded:
        logger.error("Exceeded time limit. Shutting down...")
        return


def sftp_client_init(mirror):
    ssh = paramiko.SSHClient()

    # Add host key specified to client
    host_key_raw = str.encode(mirror.ssh_host_fingerprint)
    host_key = paramiko.RSAKey(data=decodebytes(host_key_raw))
    ssh.get_host_keys().add(mirror.hostname, mirror.ssh_host_fingerprint_type, host_key)

    # Get private key
    private_key_path = f"/home/shipper/ssh/{mirror.ssh_keyfile}"
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    # Connect client
    # noinspection SpellCheckingInspection
    ssh.connect(
        hostname=mirror.hostname,
        username=mirror.ssh_username,
        pkey=private_key,
        disabled_algorithms={"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
    )
    sftp = ssh.open_sftp()
    sftp.chdir(mirror.upload_path)
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
        if elapsed_time + 30 > config.settings.CELERY_TASK_TIME_LIMIT:
            logger.warning(
                f"Task ID {task.id} is over the time limit. Manually setting as failed."
            )
            task.status = "FAILURE"
            task.save()
