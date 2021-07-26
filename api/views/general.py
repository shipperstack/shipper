from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from api.views import variant_check, parse_build_date
from shipper.models import Device, Build


class V1GeneralDeviceAll(APIView):
    """
    General endpoint to list all devices in shipper
    """
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        return_json = {}
        for device in Device.objects.all():
            variants = []

            if device.has_gapps_builds():
                variants.append("gapps")

            if device.has_vanilla_builds():
                variants.append("vanilla")

            if device.has_foss_builds():
                variants.append("foss")

            if device.has_goapps_builds():
                variants.append("goapps")

            return_json[device.codename] = {
                'status': device.status,
                'variants': variants
            }

        return Response(return_json, status=HTTP_200_OK)


class V1GeneralBuildLatest(APIView):
    """
    General endpoint for build information
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
            return Response(
                {
                    'message': "No builds exist for the specified variant yet!"
                }, status=HTTP_404_NOT_FOUND
            )

        _, version, codename, build_type, variant, date = build.file_name.split('-')

        return Response(
            {
                "datetime": int(parse_build_date(date).strftime("%s")),
                "filename": "{}.zip".format(build.file_name),
                "sha256": build.sha256sum,
                "size": build.size,
                "version": build.version,
                "variant": variant,
                "mirror_url": "https://" + request.get_host() + build.zip_file.url,
            },
            status=HTTP_200_OK
        )
