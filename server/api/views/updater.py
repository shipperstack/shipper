import html

from api.utils import variant_check, x86_type_check
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from api.views.utils import get_distributed_download_url
from config.constants import X86_DEVICE_CODENAMES
from core.models import Device


class V1UpdaterLOS(APIView):
    """
    Returns updater information that is similar in spec to what LOSUpdater expects
    """

    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request, codename, variant):
        if codename in X86_DEVICE_CODENAMES:
            return Response(
                {"message": "This endpoint is for arm devices only."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            device = get_object_or_404(Device, codename=codename)
        except Http404:
            return Response(
                {"message": "The specified device does not exist!"},
                status=HTTP_404_NOT_FOUND,
            )

        ret = variant_check(variant)
        if ret:
            return ret

        builds = device.get_all_enabled_hashed_builds_of_variant(
            variant_codename=variant
        )

        return response_from_build_query(builds, request, variant)


class V1UpdaterLOSX86(APIView):
    """
    Returns updater information that is similar in spec to what LOSUpdater expects
    """

    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request, codename, x86_type, variant):
        if codename not in X86_DEVICE_CODENAMES:
            return Response(
                {"message": "This endpoint is for x86_64 devices only."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            device = get_object_or_404(Device, codename=codename)
        except Http404:
            return Response(
                {"message": "The specified device does not exist!"},
                status=HTTP_404_NOT_FOUND,
            )

        ret = x86_type_check(x86_type)
        if ret:
            return ret

        ret = variant_check(variant)
        if ret:
            return ret

        builds = device.get_all_enabled_hashed_builds_of_type_and_variant(
            type_codename=x86_type, variant_codename=variant
        )

        return response_from_build_query(builds, request, variant, x86_type=x86_type)


def response_from_build_query(builds, request, variant, x86_type=None):
    if not builds:
        return Response(
            {"message": "No builds exist for the specified variant yet!"},
            status=HTTP_404_NOT_FOUND,
        )
    return_json = []
    for build in builds:
        build_json = {
            "datetime": int(build.build_date.strftime("%s")),
            "filename": "{}.zip".format(build.file_name),
            "id": build.sha256sum,  # WHY
            "size": build.size,
            "version": build.version,
            "variant": html.escape(variant),
            "url": get_distributed_download_url(request, build),
        }
        if x86_type is not None:
            build_json["x86_type"] = x86_type
        return_json.append(build_json)
    return Response({"response": return_json}, status=HTTP_200_OK)
