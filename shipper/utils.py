from fnmatch import fnmatch

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
