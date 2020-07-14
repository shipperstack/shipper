from django.core.exceptions import ValidationError


def validate_build_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.zip']
    if not ext in valid_extensions:
        raise ValidationError("File is of an incorrect type!")


def validate_checksum_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.md5']
    if not ext in valid_extensions:
        raise ValidationError("File is of an incorrect type!")
