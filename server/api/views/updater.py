import html
import random

from api.utils import variant_check
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from core.models import Device


class V1UpdaterLOS(APIView):
    """
    LOS-style updater endpoint
    """

    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request, codename, variant):
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

        builds = device.get_all_enabled_hashed_builds_of_variant(variant=variant)

        if not builds:
            return Response(
                {"message": "No builds exist for the specified variant yet!"},
                status=HTTP_404_NOT_FOUND,
            )

        return_json = []

        for build in builds:
            return_json.append(
                {
                    "datetime": int(build.build_date.strftime("%s")),
                    "filename": "{}.zip".format(build.file_name),
                    "id": build.sha256sum,  # WHY
                    "size": build.size,
                    "version": build.version,
                    "variant": html.escape(variant),
                    "url": get_distributed_download_url(request, build),
                }
            )

        return Response({"response": return_json}, status=HTTP_200_OK)


def get_distributed_download_url(request, build):
    if not build.is_mirrored():
        return get_main_download_url(request, build)

    available_servers = ["main", *build.get_downloadable_mirrors()]

    selected_server = random.choice(available_servers)
    match selected_server:
        case "main":
            return get_main_download_url(request, build)
        case _:
            return selected_server.get_download_url(build)


def get_main_download_url(request, build):
    return f"https://{request.get_host()}{build.zip_file.url}"
