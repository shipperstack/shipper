from django.core.exceptions import ValidationError


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.zip', '.md5']
    if not ext in valid_extensions:
        raise ValidationError("File is not supported!")

