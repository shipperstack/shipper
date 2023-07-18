import ast
import html

from django.contrib.auth import get_user_model

from api.utils import variant_check
from constance import config
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from api.views.utils import get_distributed_download_url
from core.models import Build, Device


User = get_user_model()


class V1GeneralDeviceAll(APIView):
    """
    General endpoint to list all devices in shipper
    """

    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        return_json = {}
        for device in Device.objects.all():
            variants = ast.literal_eval(config.SHIPPER_UPLOAD_VARIANTS)
            has_variants = []

            for variant in variants:
                if device.has_enabled_hashed_builds_of_variant(variant=variant):
                    has_variants.append(variant)

            return_json[device.codename] = {
                "status": device.status,
                "variants": has_variants,
            }

        return Response(return_json, status=HTTP_200_OK)


class V1GeneralMaintainerAll(APIView):
    """
    General endpoint to list all maintainer information registered with shipper
    """

    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        return_json = {}
        for user in User.objects.all():
            return_json[user.username] = {
                "active": user.is_active,
                "name": user.get_full_name(),
                "bio": user.bio,
                "profile_picture": user.profile_picture,
                "contact_url": user.contact_url,
                "devices": [device.codename for device in user.devices.all()],
            }

        return Response(return_json, status=HTTP_200_OK)


class V1GeneralMaintainerActive(APIView):
    """
    General endpoint to list active maintainer information registered with shipper
    """

    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        return_json = {}
        for user in User.objects.filter(is_active=True):
            return_json[user.username] = {
                "name": user.get_full_name(),
                "bio": user.bio,
                "profile_picture": user.profile_picture,
                "contact_url": user.contact_url,
                "devices": [device.codename for device in user.devices.all()],
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
                {"message": "The specified device does not exist!"},
                status=HTTP_404_NOT_FOUND,
            )

        ret = variant_check(variant)
        if ret:
            return ret

        try:
            build = device.get_latest_enabled_hashed_build_of_variant(variant=variant)
        except Build.DoesNotExist:
            return Response(
                {"message": "No builds exist for the specified variant yet!"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "datetime": int(build.build_date.strftime("%s")),
                "filename": "{}.zip".format(build.file_name),
                "sha256": build.sha256sum,
                "size": build.size,
                "version": build.version,
                "variant": html.escape(variant),
                "mirror_url": get_distributed_download_url(request, build),
            },
            status=HTTP_200_OK,
        )
