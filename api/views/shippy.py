import os

from django.contrib.auth import authenticate

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from drf_chunked_upload.exceptions import ChunkedUploadError
from drf_chunked_upload.settings import CHECKSUM_TYPE
from drf_chunked_upload.views import ChunkedUploadView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND

from config.settings import SHIPPER_VERSION
from shipper.exceptions import UploadException
from shipper.handler import handle_chunked_build
from shipper.models import Device, Build
from shipper.views import exception_to_message


class V1MaintainersChunkedUpload(ChunkedUploadView):
    def _post(self, request, pk=None, *args, **kwargs):
        chunked_upload = None
        if pk:
            upload_id = pk
        else:
            chunked_upload = self._put_chunk(request, *args,
                                             whole=True, **kwargs)
            upload_id = chunked_upload.id

        checksum = request.data.get(CHECKSUM_TYPE)

        error_msg = None
        if self.do_checksum_check:
            if not upload_id or not checksum:
                error_msg = ("Both 'id' and '{}' are "
                             "required").format(CHECKSUM_TYPE)
        elif not upload_id:
            error_msg = "'id' is required"
        if error_msg:
            raise ChunkedUploadError(status=HTTP_400_BAD_REQUEST,
                                     detail=error_msg)

        if not chunked_upload:
            chunked_upload = get_object_or_404(self.get_queryset(),
                                               pk=upload_id)

        self.is_valid_chunked_upload(chunked_upload)

        if self.do_checksum_check:
            self.checksum_check(chunked_upload, checksum)

        chunked_upload.completed()

        device_codename = get_codename_from_filename(chunked_upload.filename)
        device = get_object_or_404(Device, codename=device_codename)

        # Check if maintainer is in device's approved maintainers list
        if self.request.user not in device.maintainers.all():
            chunked_upload.delete()
            return Response(
                {
                    'error': 'insufficient_permissions',
                    'message': 'You are not authorized to upload for this device!'
                },
                status=HTTP_401_UNAUTHORIZED
            )

        try:
            build_id = handle_chunked_build(device, chunked_upload, request.POST.get('md5'))
        except UploadException as exception:
            chunked_upload.delete()
            return Response(
                {
                    'error': str(exception),
                    'message': exception_to_message(exception)
                },
                status=HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'message': 'Build has been uploaded for device {}!'.format(device),
                'build_id': build_id
            },
            status=HTTP_200_OK
        )


def get_codename_from_filename(filename):
    fields = os.path.splitext(filename)[0].split('-')
    # Check field count
    if len(fields) != 6:
        return None
    return fields[2]  # Codename


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def v1_maintainers_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {
                'error': 'blank_username_or_password',
                'message': 'Username or password cannot be blank!'
            },
            status=HTTP_400_BAD_REQUEST
        )
    user = authenticate(username=username, password=password)
    if not user:
        return Response({
            'error': 'invalid_credential',
            'message': 'Invalid credentials. Please try again.'
        },
            status=HTTP_404_NOT_FOUND
        )
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key,
            'message': 'Successfully logged in!'
        },
        status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_system_info(request):
    return Response(
        {
            'version': SHIPPER_VERSION
        }
    )


@csrf_exempt
@api_view(["GET"])
def v1_maintainers_token_check(request):
    return Response(
        {
            'username': request.user.username
        },
        status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["GET"])
def v1_maintainers_build_enabled_status_modify(request):
    build_id = request.data.get("build_id")
    enable = request.data.get("enable").lower() == "true"
    if build_id is None or enable is None:
        return Response(
            {
                'error': 'missing_parameters',
                'message': 'One or more of the required parameters is blank! Required parameters: build ID, '
                           'enabled flag'
            },
            status=HTTP_400_BAD_REQUEST
        )

    build = get_object_or_404(Build, pk=build_id)

    # Check if maintainer has permission to modify this build/device
    if request.user not in build.device.maintainers.all():
        return Response(
            {
                'error': 'insufficient_permissions',
                'message': 'You are not authorized to modify builds associated with this device!'
            },
            status=HTTP_401_UNAUTHORIZED
        )

    # Switch build status
    build.enabled = enable
    build.save()

    if enable:
        return Response(
            {
                'message': 'Successfully enabled the build!'
            },
            status=HTTP_200_OK
        )
    else:
        return Response(
            {
                'message': 'Successfully disabled the build!'
            },
            status=HTTP_200_OK
        )
