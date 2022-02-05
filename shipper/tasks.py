import hashlib
import os
import time
from contextlib import contextmanager

import humanize
# noinspection PyPackageRequirements
import paramiko
import pysftp
# noinspection PyPackageRequirements
from billiard.exceptions import TimeLimitExceeded
from celery import shared_task
from django.core.cache import cache
from django.db import transaction
# noinspection PyPackageRequirements
from paramiko.py3compat import decodebytes

from config import settings

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
    for build in Build.objects.filter(sha256sum__exact=''):
        generate_sha256.delay(build.id)

    for build in Build.objects.all():
        if not build.is_mirrored():
            mirror_build.delay(build.id)


@shared_task(bind=True, default_retry_delay=60 * 60, autoretry_for=(TimeLimitExceeded,), retry_backoff=True)
def mirror_build(self, build_id):
    build = Build.objects.get(id=build_id)

    # Setup lock
    lock_id = '{}-lock-{}'.format(self.name, build.id)
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

                if not is_version_in_target_versions(build.version, mirror.target_versions):
                    continue

                keydata = str.encode(mirror.ssh_host_fingerprint)
                key = paramiko.RSAKey(data=decodebytes(keydata))
                cnopts = pysftp.CnOpts()
                cnopts.hostkeys.add(mirror.hostname, mirror.ssh_host_fingerprint_type, key)

                with pysftp.Connection(
                        host=mirror.hostname,
                        username=mirror.ssh_username,
                        private_key='/home/shipper/ssh/{}'.format(mirror.ssh_keyfile),
                        cnopts=cnopts
                ) as sftp:
                    sftp.cwd(mirror.upload_path)

                    if not sftp.exists(build.device.codename):
                        sftp.mkdir(build.device.codename)

                    sftp.cwd(build.device.codename)

                    def print_progress(transferred, total):
                        print(
                            "{} transferred out of {} ({:.2f}%)".format(
                                humanize.naturalsize(transferred), humanize.naturalsize(total),
                                transferred * 100 / total
                            ))

                    sftp.put(
                        os.path.join(settings.MEDIA_ROOT, build.zip_file.name),
                        callback=lambda x, y: print_progress(x, y),
                    )
                    sftp.put(os.path.join(settings.MEDIA_ROOT, build.md5_file.name))

                # Fetch build one more time and lock until save completes
                with transaction.atomic():
                    build = Build.objects.select_for_update().get(id=build_id)
                    build.mirrored_on.add(mirror)
                    build.save()
        else:
            print(f"Build {build.file_name} is already being mirrored by another process, exiting!")


@shared_task
def generate_sha256(build_id):
    build = Build.objects.get(id=build_id)

    # Check if this task has already been run
    if build.sha256sum not in [None, '']:
        print(f"Build {build.file_name}'s SHA256 generated by another process, exiting!")
        return

    sha256sum = hashlib.sha256()
    with open(os.path.join(settings.MEDIA_ROOT, build.zip_file.name), 'rb') as destination:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: destination.read(4096), b""):
            sha256sum.update(byte_block)

    # Lock build and update SHA256 hash
    with transaction.atomic():
        Build.objects.select_for_update().filter(id=build_id).update(sha256sum=sha256sum.hexdigest())
