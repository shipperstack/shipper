import ast

from constance import config
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def variant_check(variant):
    variants = ast.literal_eval(config.SHIPPER_UPLOAD_VARIANTS)
    if variant not in variants:
        return Response(
            {"message": "Wrong parameter. Try with the correct parameters."},
            status=HTTP_400_BAD_REQUEST,
        )
