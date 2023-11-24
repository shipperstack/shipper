from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from core.models import Variant


def variant_check(variant):
    variant_codenames = [variant.codename for variant in Variant.objects.all()]
    if variant not in variant_codenames:
        return Response(
            {"message": "Wrong parameter. Try with the correct parameters."},
            status=HTTP_400_BAD_REQUEST,
        )
