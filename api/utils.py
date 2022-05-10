import ast

from constance import config
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
    variants = ast.literal_eval(config.SHIPPER_UPLOAD_VARIANTS)
    if variant not in variants:
        return Response(
            {"message": "Wrong parameter. Try with the correct parameters."},
            status=HTTP_400_BAD_REQUEST,
        )
