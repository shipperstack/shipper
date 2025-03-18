import re
from fnmatch import fnmatch

from constance import config

from .exceptions import UploadException


def is_version_in_target_versions(version, target_versions):
    if target_versions == "":
        return False

    if target_versions == "*":
        return True

    # Raise exception if supplied version includes a wildcard character
    if "*" in version:
        raise Exception("version-has-wildcard")

    target_versions = target_versions.splitlines()
    for target_version in target_versions:
        if "*" in target_version:
            # Wildcard matching
            if fnmatch(version, target_version):
                return True
        else:
            if version == target_version:
                return True
    return False


def parse_filename_with_regex(filename):
    pattern = re.compile(config.SHIPPER_FILE_NAME_FORMAT)
    matches = pattern.search(filename)

    if not matches:
        raise UploadException(
            {"error": "invalid_file_name", "message": "The file name is malformed!"}
        )

    return matches.groupdict()
