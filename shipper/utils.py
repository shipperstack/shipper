import re
from fnmatch import fnmatch

from django.conf import settings

from .exceptions import RegexParseException


def is_version_in_target_versions(version, target_versions):
    if target_versions == "":
        return False

    if target_versions == "*":
        return True

    # Raise exception if supplied version includes a wildcard character
    if "*" in version:
        raise Exception

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
    pattern = re.compile(settings.SHIPPER_FILE_NAME_FORMAT)
    matches = pattern.search(filename)

    if not matches:
        raise RegexParseException("invalid_file_name")

    return {
        "version": matches.group("version"),
        "codename": matches.group("codename"),
        "variant": matches.group("variant"),
        "date": matches.group("date"),
    }
