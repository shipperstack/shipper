import html

from constance import config
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from drf_chunked_upload.exceptions import ChunkedUploadError
from drf_chunked_upload.serializers import ChunkedUploadSerializer
from drf_chunked_upload.views import ChunkedUploadView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from core.exceptions import UploadException
from api.handler import handle_chunked_build
from core.models import Build, Device, Variant
from core.utils import parse_filename_with_regex


# Serializer for overriding success url
class V1MaintainersChunkedUploadSerializer(ChunkedUploadSerializer):
    # noinspection SpellCheckingInspection
    viewname = "v1_maintainers_chunked_upload_detail"


class V1MaintainersChunkedUpload(ChunkedUploadView):
    """
    Internal endpoint used by shippy to chunk-upload build artifacts
    """

    serializer_class = V1MaintainersChunkedUploadSerializer

    def post(self, request, pk=None, *args, **kwargs):
        """
        Handle POST requests.
        """
        try:
            return self._post(request, *args, pk=pk, **kwargs)
        except ChunkedUploadError as error:
            # Delete chunked upload (if it exists)
            if pk:
                try:
                    chunked_upload = get_object_or_404(self.get_queryset(), pk=pk)
                    chunked_upload.delete()
                except Http404:
                    pass
            return Response(error.data, status=error.status_code)

    def on_completion(self, chunked_upload, request) -> Response:
        """
        Validates chunked upload and transfers to handler
        """
        try:
            device_codename = parse_filename_with_regex(chunked_upload.filename)[
                "codename"
            ]
            device = Device.objects.get(codename=device_codename)
        except Device.DoesNotExist:
            chunked_upload.delete()
            return Response(
                {
                    "error": "unknown_device",
                    "message": "The specified device does not exist!",
                },
                status=HTTP_404_NOT_FOUND,
            )
        except UploadException as exception:
            chunked_upload.delete()
            return Response(
                exception.args[0],
                status=HTTP_400_BAD_REQUEST,
            )

        # Check if maintainer is in device's approved maintainers list
        if (
            not self.request.user.full_access_to_devices
            and self.request.user not in device.maintainers.all()
        ):
            chunked_upload.delete()
            return Response(
                {
                    "error": "insufficient_permissions",
                    "message": "You are not authorized to upload for this device!",
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        try:
            build_id = handle_chunked_build(device, chunked_upload)
        except UploadException as exception:
            chunked_upload.delete()
            return Response(
                exception.args[0],
                status=HTTP_400_BAD_REQUEST,
            )

        # Upload was successful, update user's last login timestamp
        update_last_login(None, self.request.user)

        return Response(
            {
                "message": "Build has been uploaded for device {}!".format(device),
                "build_id": build_id,
            },
            status=HTTP_200_OK,
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def v1_maintainers_login(request):
    """
    Returns a token when passed login details for a maintainer

    :param request: data must include `username` and `password`
    :return: an API token
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {
                "error": "blank_username_or_password",
                "message": "Username or password cannot be blank!",
            },
            status=HTTP_400_BAD_REQUEST,
        )
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {
                "error": "invalid_credential",
                "message": "Invalid credentials. Please try again.",
            },
            status=HTTP_404_NOT_FOUND,
        )

    # Update login timestamp
    update_last_login(None, user)

    # Generate and return token
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "message": "Successfully logged in!"}, status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v2_system_info(_):
    """
    Returns shipper system information

    :return: the current shipper system information
    """
    variants = {v.codename: v.description for v in Variant.objects.all()}
    return Response(
        {
            "version": settings.SHIPPER_VERSION,
            "shippy_compat_version": settings.SHIPPER_SHIPPY_COMPAT_VERSION,
            "shippy_upload_checksum_type": settings.DRF_CHUNKED_UPLOAD_CHECKSUM,
            "shippy_allowed_versions": config.SHIPPER_ALLOWED_VERSIONS_TO_UPLOAD,
            "shippy_upload_variants": variants,
        }
    )


@never_cache
@csrf_exempt
@api_view(["GET"])
def v1_maintainers_token_check(request):
    """
    Checks whether a given API token is still valid or not

    :param request: the token must be supplied via an authorization header
    :return: The username if the token is still valid, or an HTTP error code otherwise
    """
    # Update login timestamp
    update_last_login(None, request.user)

    return Response(
        {"username": html.escape(request.user.username)}, status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["GET"])
def v1_maintainers_upload_filename_regex_pattern(request):
    """
    Returns the upload filename regex pattern defined by the server administrators

    :param request: the token must be supplied via an authorization header
    :return: The upload filename regex pattern
    """
    # Update login timestamp
    update_last_login(None, request.user)

    return Response({"pattern": config.SHIPPER_FILE_NAME_FORMAT}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def v1_maintainers_build_duplicate_check(request):
    """
    Checks if the given build already exists in the system

    :param request: data must include `file_name`
    :return: Whether the build exists or not
    """
    file_name = request.data.get("file_name")
    if file_name is None:
        return Response(
            {
                "error": "missing_parameters",
                "message": "The required parameter `file_name` was not provided.",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    exists = Build.objects.filter(file_name=file_name).exists()

    return Response({"exists": exists})


@csrf_exempt
@api_view(["POST"])
def v1_maintainers_build_enabled_status_modify(request):
    """
    Modifies the given build's enabled status

    :param request: data must include `build_id` and `enable`
    :return: Whether the build was enabled or disabled
    """
    build_id = request.data.get("build_id")
    enable = request.data.get("enable")
    if build_id is None or enable is None:
        return Response(
            {
                "error": "missing_parameters",
                "message": "One or more of the required parameters is blank! Required "
                "parameters: build ID, enabled flag",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    try:
        build = get_object_or_404(Build, pk=build_id)
    except ValueError:
        return Response(
            {
                "error": "invalid_parameters",
                "message": "The specified build ID is invalid.",
            },
            status=HTTP_400_BAD_REQUEST,
        )
    enable = enable.lower() == "true"

    # Check if maintainer has permission to modify this build/device
    if request.user not in build.device.maintainers.all():
        return Response(
            {
                "error": "insufficient_permissions",
                "message": "You are not authorized to modify builds associated with "
                "this device!",
            },
            status=HTTP_401_UNAUTHORIZED,
        )

    # Switch build status
    build.enabled = enable
    build.save()

    # Update login timestamp
    update_last_login(None, request.user)

    if enable:
        return Response(
            {"message": "Successfully enabled the build!"}, status=HTTP_200_OK
        )
    else:
        return Response(
            {"message": "Successfully disabled the build!"}, status=HTTP_200_OK
        )
