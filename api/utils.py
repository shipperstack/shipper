from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def variant_check(variant):
    if variant not in settings.SHIPPER_UPLOAD_VARIANTS:
        return Response(
            {"message": "Wrong parameter. Try with the correct parameters."},
            status=HTTP_400_BAD_REQUEST,
        )


def exception_to_message(e):
    e = str(e)
    if e == "file_name_mismatch":
        return "The file name does not match the checksum file name!"
    if e == "invalid_file_name":
        return "The file name was malformed. Please do not edit the file name!"
    if e == "not_official":
        return "Only official builds are allowed."
    if e == "codename_mismatch":
        return "The codename does not match the file!"
    if e == "duplicate_build":
        return "The build already exists in the system!"
    return "An unknown error occurred."
