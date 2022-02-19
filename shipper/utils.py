import re

from fnmatch import fnmatch

from config import settings

def is_version_in_target_versions(version, target_versions):
    if target_versions == "":
        return False

    if target_versions == "*":
        return True

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
    m = p.search(filename)

    if not m:
        raise RegexParseException('invalid_file_name')

    return {'version': m.group("version"), 'codename': m.group("codename"), 'variant': m.group("variant"), 'date': m.group("date")}
