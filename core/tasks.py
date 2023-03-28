import hashlib
import os
import time
from contextlib import contextmanager

import paramiko
from billiard.exceptions import TimeLimitExceeded
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from base64 import decodebytes

from constance import config

from celery import shared_task

from .models import Build, MirrorServer
from .utils import is_version_in_target_versions


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + settings.CELERY_TASK_TIME_LIMIT - 3
    status = cache.add(lock_id, oid, settings.CELERY_TASK_TIME_LIMIT)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@shared_task
def process_incomplete_builds():
    for build in [build for build in Build.objects.all() if not build.is_hashed()]:
        generate_checksum.delay(build.id)

    for build in [build for build in Build.objects.all() if not build.is_mirrored()]:
        mirror_build.delay(build.id)


@shared_task(
    bind=True,
    default_retry_delay=60 * 60,
    autoretry_for=(TimeLimitExceeded,),
    retry_backoff=True,
)
def mirror_build(self, build_id):
    build = Build.objects.get(id=build_id)

    # Setup lock
    lock_id = "{}-lock-{}".format(self.name, build.id)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            mirrors = MirrorServer.objects.filter(enabled=True)

            if len(mirrors) == 0:
                print("No mirror servers found to mirror to. Exiting...")
                return

            for mirror in mirrors:
                # Check if a previous run has already completed a backup
                if mirror in build.mirrored_on.all():
                    continue

                if not is_version_in_target_versions(
                    build.version, mirror.target_versions
                ):
                    continue

                ssh = paramiko.SSHClient()

                # Add host key specified to client
                host_key_raw = str.encode(mirror.ssh_host_fingerprint)
                host_key = paramiko.RSAKey(data=decodebytes(host_key_raw))
                ssh.get_host_keys().add(
                    mirror.hostname, mirror.ssh_host_fingerprint_type, host_key
                )

                # Get private key
                private_key_path = f"/home/shipper/ssh/{mirror.ssh_keyfile}"
                private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

                # Connect client
                ssh.connect(
                    hostname=mirror.hostname,
                    username=mirror.ssh_username,
                    pkey=private_key,
                    disabled_algorithms={"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
                )
                sftp = ssh.open_sftp()
                sftp.chdir(mirror.upload_path)

                # Check if device directory exists and change into it
                try:
                    sftp.stat(build.device.codename)
                except FileNotFoundError:
                    sftp.mkdir(build.device.codename)
                sftp.chdir(build.device.codename)

                # Define callback for printing progress
                def update_progress(transferred, total):
                    # TODO: Remove and unindent this once debugging complete
                    if config.SHIPPER_CELERY_UPLOAD_UPDATE_PROGRESS:
                        self.update_state(
                            meta={"current": transferred, "total": total},
                        )

                # Start upload
                # Upload build zip file
                try:
                    sftp.put(
                        localpath=os.path.join(
                            settings.MEDIA_ROOT, build.zip_file.name
                        ),
                        remotepath=f"{build.file_name}.zip",
                        callback=update_progress,
                    )
                except Exception as exception:
                    # Mark task as failed and stop
                    self.update_state(state="FAILURE", meta={"exception": exception})
                    return

                # Fetch build one more time and lock until save completes
                with transaction.atomic():
                    build = Build.objects.select_for_update().get(id=build_id)
                    build.mirrored_on.add(mirror)
                    build.save()
        else:
            print(
                f"Build {build.file_name} is already being mirrored by another process!"
            )


def update_hash(hash_type, build):
    with open(
        os.path.join(settings.MEDIA_ROOT, build.zip_file.name), "rb"
    ) as destination:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: destination.read(4096), b""):
            hash_type.update(byte_block)


@shared_task
def generate_checksum(build_id):
    build = Build.objects.get(id=build_id)

    # Check if MD5 is already generated
    if build.md5sum not in [None, ""]:
        print(f"Build {build.file_name}'s MD5 generated by another process!")
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
        print(f"Build {build.file_name}'s SHA256 generated by another process!")
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
)
def delete_mirrored_build(self, build_id, mirrorserver_id):
    build = Build.objects.get(id=build_id)

    # Setup lock
    lock_id = "{}-lock-{}".format(self.name, build.id)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            mirror = MirrorServer.objects.get(id=mirrorserver_id)

            if mirror not in build.mirrored_on.all():
                print(
                    f"Build {build.file_name} is not mirrored on mirror server {mirror.name}!"
                )

            ssh = paramiko.SSHClient()

            # Add host key specified to client
            host_key_raw = str.encode(mirror.ssh_host_fingerprint)
            host_key = paramiko.RSAKey(data=decodebytes(host_key_raw))
            ssh.get_host_keys().add(
                mirror.hostname, mirror.ssh_host_fingerprint_type, host_key
            )

            # Get private key
            private_key_path = f"/home/shipper/ssh/{mirror.ssh_keyfile}"
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

            # Connect client
            ssh.connect(
                hostname=mirror.hostname,
                username=mirror.ssh_username,
                pkey=private_key,
                disabled_algorithms={"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
            )
            sftp = ssh.open_sftp()
            sftp.chdir(mirror.upload_path)

            # Check if device directory exists and change into it
            try:
                sftp.stat(build.device.codename)
            except FileNotFoundError:
                print("The device directory does not exist on the mirror server!")
                return

            # Delete build from server
            sftp.delete(remotepath=f"{build.file_name}.zip")

            # Fetch build one more time and lock until save completes
            with transaction.atomic():
                build = Build.objects.select_for_update().get(id=build_id)
                build.mirrored_on.remove(mirror)
                build.save()
        else:
            print(
                f"Build {build.file_name} is already being deleted from the mirror server by another process!"
            )
