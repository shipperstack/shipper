import os
from pathlib import Path
from config import settings

from .models import Build
from .tasks import process_build


def handle_builds(device, build_file, checksum_file, gapps, release):
    # Confirm file names of build and checksum files match
    checksum_file_name, checksum_file_ext = os.path.splitext(checksum_file.name)
    if build_file.name != checksum_file_name:
        raise Exception('file_name_mismatch')

    build_file_name, build_file_ext = os.path.splitext(build_file.name)
    try:
        _, version, codename, type, date = build_file_name.split('-')
    except:
        raise Exception('invalid_file_name')

    if codename != device.codename:
        raise Exception('codename_mismatch')

    if Build.objects.filter(file_name=build_file_name).count() >= 1:
        raise Exception('duplicate_build')

    # Start upload
    Path(os.path.join(settings.MEDIA_ROOT, device.codename)).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(settings.MEDIA_ROOT, device.codename, build_file.name), 'wb+') as destination:
        for chunk in build_file.chunks():
            destination.write(chunk)

    with open(os.path.join(settings.MEDIA_ROOT, device.codename, checksum_file.name), 'wb+') as destination:
        for chunk in checksum_file.chunks():
            destination.write(chunk)

    build = Build(
        device=device,
        file_name=build_file_name,
        size=build_file.size,
        version=version,
        sha256sum="0",
        gapps=gapps,
        release=release
    )
    build.save()

    process_build.delay(device.codename)