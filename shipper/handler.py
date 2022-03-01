import os
from datetime import datetime

from django.conf import settings

from .exceptions import UploadException
from .models import Build
from .tasks import generate_sha256, mirror_build
from .utils import parse_filename_with_regex


def handle_chunked_build(device, chunked_file, md5_value):
    # Parse file name
    filename_parts = parse_filename_with_regex(chunked_file.filename)

    # Check for duplicate builds
    if (
        Build.objects.filter(
            file_name=os.path.splitext(chunked_file.filename)[0]
        ).count()
        >= 1
    ):
        raise UploadException("duplicate_build")

    # Check if variant is supported
    if filename_parts["variant"] not in settings.SHIPPER_UPLOAD_VARIANTS:
        raise UploadException("invalid_file_name")

    # Construct full path to save files in
    target_file_full_path = os.path.join(
        settings.MEDIA_ROOT, device.codename, chunked_file.filename
    )

    # See if the build exists from a previous failed attempt
    if os.path.exists(target_file_full_path):
        os.remove(target_file_full_path)

    # Make sure device codename folder exists
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, device.codename)):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, device.codename))

    # Rename chunked file and move to correct folder
    os.rename(chunked_file.file.path, target_file_full_path)

    # Generate MD5 file
    md5_file_contents = "{}  {}".format(md5_value, chunked_file.filename)
    with open(
        os.path.join(
            settings.MEDIA_ROOT, device.codename, f"{chunked_file.filename}.md5"
        ),
        "w",
    ) as target_md5:
        target_md5.write(md5_file_contents)

    # Construct and save build object in database
    build = Build(
        device=device,
        file_name=os.path.splitext(chunked_file.filename)[0],
        size=os.path.getsize(target_file_full_path),
        version=filename_parts["version"],
        variant=filename_parts["variant"],
        build_date=datetime.strptime(filename_parts["date"], "%Y%m%d"),
        zip_file="{}/{}".format(device.codename, chunked_file.filename),
        md5_file="{}/{}.md5".format(device.codename, chunked_file.filename),
        enabled=True,
    )
    build.save()

    # Delete unused chunked_upload file
    chunked_file.delete()

    # Execute background tasks
    generate_sha256.delay(build.id)
    mirror_build.delay(build.id)

    return build.id
