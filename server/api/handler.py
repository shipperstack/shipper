import os
from datetime import datetime

from django.conf import settings
from constance import config

from config.constants import X86_DEVICE_CODENAMES
from core.exceptions import UploadException
from core.models import Build, Variant, X86Type
from core.tasks import generate_checksum, mirror_build
from core.utils import parse_filename_with_regex, is_version_in_target_versions


def handle_chunked_build(device, chunked_file):
    # Parse file name
    filename_parts = parse_filename_with_regex(chunked_file.filename)

    # Check for duplicate builds
    if (
        Build.objects.filter(
            file_name=os.path.splitext(chunked_file.filename)[0]
        ).count()
        >= 1
    ):
        raise UploadException(
            {
                "error": "duplicate_build",
                "message": "The build already exists in the system!",
            }
        )

    # Check if variant is supported
    variant_codenames = [variant.codename for variant in Variant.objects.all()]
    if filename_parts["variant"] not in variant_codenames:
        raise UploadException(
            {
                "error": "unsupported_variant",
                "message": "The build's variant is not supported by this server "
                "instance. If you believe the variant is valid, please contact an "
                "admin to change the allowed variants list.",
            }
        )

    # If x86, check for x86 type
    if filename_parts["codename"] in X86_DEVICE_CODENAMES:
        x86_type_codenames = [x.codename for x in X86Type.objects.all()]
        if filename_parts["x86_type"] not in x86_type_codenames:
            raise UploadException(
                {
                    "error": "unsupported_x86_type",
                    "message": "The build's x86 type is not supported by this server "
                    "instance. If you believe the x86 type is valid, please contact an "
                    "admin to change the allowed x86 types list.",
                }
            )

    # Check if version is in allowed versions list
    if not is_version_in_target_versions(
        filename_parts["version"], config.SHIPPER_ALLOWED_VERSIONS_TO_UPLOAD
    ):
        raise UploadException(
            {
                "error": "version_not_allowed",
                "message": "The server is currently not accepting this build's"
                f"version, {filename_parts['version']}. The server only accepts the "
                f"following versions: {config.SHIPPER_ALLOWED_VERSIONS_TO_UPLOAD}. "
                "If you believe the version should be allowed, please contact an "
                "admin to adjust server settings.",
            }
        )

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

    # Construct and save build object in database
    build = Build(
        device=device,
        file_name=os.path.splitext(chunked_file.filename)[0],
        size=os.path.getsize(target_file_full_path),
        version=filename_parts["version"],
        variant=filename_parts["variant"],
        build_date=datetime.strptime(filename_parts["date"], "%Y%m%d"),
        zip_file="{}/{}".format(device.codename, chunked_file.filename),
        enabled=True,
    )
    if filename_parts["codename"] in X86_DEVICE_CODENAMES:
        build.x86_type = X86Type.objects.get(codename=filename_parts["x86_type"])

    build.save()

    # Delete unused chunked_upload file
    chunked_file.delete()

    # Execute background tasks
    generate_checksum.delay(build.id)
    mirror_build.delay(build.id)

    return build.id
