import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from shipper.models import Build, Device


def variant_check(variant):
    if variant not in ["gapps", "vanilla", "foss", "goapps"]:
        return Response(
            {
                'message': "Wrong parameter. Try with the correct parameters."
            }, status=HTTP_400_BAD_REQUEST
        )


class V1UpdaterLOS(APIView):
    """
    LOS-style endpoint used by updater app (possibly not used anymore?)
    """
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request, codename, variant):
        try:
            device = get_object_or_404(Device, codename=codename)
        except Http404:
            return Response(
                {
                    'message': "The specified device does not exist!"
                }, status=HTTP_404_NOT_FOUND
            )

        ret = variant_check(variant)
        if ret:
            return ret

        builds = None
        if variant == "gapps":
            builds = device.get_all_gapps_build_objects()
        elif variant == "vanilla":
            builds = device.get_all_vanilla_build_objects()
        elif variant == "foss":
            builds = device.get_all_foss_build_objects()
        elif variant == "goapps":
            builds = device.get_all_goapps_build_objects()

        # Check if list is empty and return a 404
        if not builds:
            return Response(
                {
                    'message': "No builds exist for the specified variant yet!"
                }, status=HTTP_404_NOT_FOUND
            )

        return_json = []

        for build in builds:
            _, version, codename, build_type, variant, date = build.file_name.split('-')

            date = parse_build_date(date)

            return_json.append({
                "datetime": int(date.strftime("%s")),
                "filename": "{}.zip".format(build.file_name),
                "id": build.sha256sum,  # WHY
                "size": build.size,
                "version": build.version,
                "variant": variant,
                "url": "https://" + request.get_host() + build.zip_file.url,
                "md5url": "https://" + request.get_host() + build.md5_file.url,
            })

        return Response(
            {"response": return_json},
            status=HTTP_200_OK
        )


class V2UpdaterDevice(APIView):
    """
    Updater endpoint used by the R updater
    """
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request, codename, variant):
        """Updater endpoint used by the R updater"""
        try:
            device = get_object_or_404(Device, codename=codename)
        except Http404:
            return Response(
                {
                    'message': "The specified device does not exist!"
                }, status=HTTP_404_NOT_FOUND
            )

        ret = variant_check(variant)
        if ret:
            return ret

        build = None
        try:
            if variant == "gapps":
                build = device.get_latest_gapps_build_object()
            elif variant == "vanilla":
                build = device.get_latest_vanilla_build_object()
            elif variant == "foss":
                build = device.get_latest_foss_build_object()
            elif variant == "goapps":
                build = device.get_latest_goapps_build_object()
        except Build.DoesNotExist:
            raise Http404("No builds exist for the specified variant yet!")

        _, version, _, _, _, date = build.file_name.split('-')

        date = parse_build_date(date)

        return Response(
            {
                "date": int(date.strftime("%s")),
                "file_name": "{}.zip".format(build.file_name),
                "sha256": build.sha256sum,
                "size": build.size,
                "version": build.version,
                "zip_download_url": "https://" + request.get_host() + build.zip_file.url,
                "md5_download_url": "https://" + request.get_host() + build.md5_file.url,
            }, status=HTTP_200_OK
        )


def parse_build_date(date):
    year = int(date[:4])
    month = int(date[4:-2])
    day = int(date[6:])

    return datetime.date(year, month, day)
