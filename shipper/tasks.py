import hashlib
import os
import time
from contextlib import contextmanager

import humanize
import paramiko
from billiard.exceptions import TimeLimitExceeded
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from paramiko.py3compat import decodebytes

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
                ssh.get_host_keys().add(mirror.hostname, mirror.ssh_host_fingerprint_type, host_key)

                # Get private key
                private_key_path = f"/home/shipper/ssh/{mirror.ssh_keyfile}"
                private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

                # Connect client
                ssh.connect(
                    hostname=mirror.hostname,
                    username=mirror.ssh_username,
                    pkey=private_key
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
                def print_progress(transferred, total):
                    print(
                        "{} transferred out of {} ({:.2f}%)".format(
                            humanize.naturalsize(transferred),
                            humanize.naturalsize(total),
                            transferred * 100 / total,
                        )
                    )

                # Start upload
                # Upload build zip file
                sftp.put(
                    localpath=os.path.join(settings.MEDIA_ROOT, build.zip_file.name),
                    remotepath=build.zip_file.name,
                    callback=print_progress,
                )
                # Upload build checksum
                sftp.put(
                    localpath=os.path.join(settings.MEDIA_ROOT, build.md5_file.name),
                    remotepath=build.md5_file.name
                )

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
        print(
            f"Build {build.file_name}'s MD5 generated by another process!"
        )
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
        print(
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
