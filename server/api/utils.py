from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from core.models import Variant, X86Type

WRONG_PARAMETER_RESPONSE = Response(
    {"message": "Wrong parameter. Try with the correct parameters."},
    status=HTTP_400_BAD_REQUEST,
)


def variant_check(variant):
    variant_codenames = [variant.codename for variant in Variant.objects.all()]
    if variant not in variant_codenames:
        return WRONG_PARAMETER_RESPONSE


def x86_type_check(x86_type):
    type_codenames = [x86_type.codename for x86_type in X86Type.objects.all()]
    if x86_type not in type_codenames:
        return WRONG_PARAMETER_RESPONSE
