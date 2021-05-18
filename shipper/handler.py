import hashlib
import os
from config import settings

from .models import Build
from .exceptions import *


def handle_build(device, zip_file, md5_file, md5_value=None):
    # Confirm file names of build and checksum files match
    checksum_file_name, checksum_file_ext = os.path.splitext(md5_file.name)
    if zip_file.name != checksum_file_name:
        raise UploadException('file_name_mismatch')

    build_file_name, build_file_ext = os.path.splitext(zip_file.name)
    try:
        _, version, codename, build_type, variant, date = build_file_name.split('-')
    except ValueError:
        raise UploadException('invalid_file_name')

    if build_type != "OFFICIAL":
        raise UploadException('not_official')

    if codename != device.codename:
        raise UploadException('codename_mismatch')

    if Build.objects.filter(file_name=build_file_name).count() >= 1:
        raise UploadException('duplicate_build')

    # See if a file exists from a previous failed attempt
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, device.codename, zip_file.name)):
        os.remove(os.path.join(settings.MEDIA_ROOT, device.codename, zip_file.name))

    if os.path.exists(os.path.join(settings.MEDIA_ROOT, device.codename, md5_file.name)):
        os.remove(os.path.join(settings.MEDIA_ROOT, device.codename, md5_file.name))

    if variant not in ["gapps", "vanilla", "foss", "goapps"]:
        raise UploadException('invalid_file_name')

    build = Build(
        device=device,
        file_name=build_file_name,
        size=zip_file.size,
        version=version,
        variant=variant,
        zip_file=zip_file,
        md5_file=md5_file
    )

    # Save the files FIRST
    build.save()

    # If the files were uploaded using chunked upload, then we need to manually create an MD5 file
    if md5_file is None:
        # Generate string
        md5_file_contents = "{}  {}".format(md5_value, zip_file.name)
        with open(os.path.join(settings.MEDIA_ROOT, device.codename, "{}.md5".format(zip_file.name)), 'w')\
                as target_md5:
            target_md5.write(md5_file_contents)

    # Process SHA256
    sha256sum = hashlib.sha256()
    with open(os.path.join(settings.MEDIA_ROOT, device.codename, zip_file.name), 'rb') as destination:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: destination.read(4096), b""):
            sha256sum.update(byte_block)
    build.sha256sum = sha256sum.hexdigest()

    build.save()
