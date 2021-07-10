import json
import os

from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_chunked_upload.exceptions import ChunkedUploadError
from drf_chunked_upload.response import Response
from drf_chunked_upload.settings import CHECKSUM_TYPE
from drf_chunked_upload.views import ChunkedUploadView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from config.settings import SHIPPER_VERSION
from shipper.exceptions import UploadException
from shipper.handler import handle_chunked_build
from shipper.models import *
from shipper.views import exception_to_message


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def v1_download_build_counter(request):
    file_name = request.data.get("file_name")

    if file_name:
        try:
            build = Build.objects.get(file_name=file_name)
            build_increase_download_count(build)
            return Response(
                {
                    'message': 'The request was successful!'
                },
                status=HTTP_200_OK
            )
        except Build.DoesNotExist:
            return Response(
                {
                    'error': 'invalid_build_name',
                    'message': 'A build with that file name does not exist!'
                },
                status=HTTP_404_NOT_FOUND
            )

    build_id = request.data.get("build_id")

    if build_id:
        try:
            build = Build.objects.get(pk=int(build_id))
            build_increase_download_count(build)
            return Response(
                {
                    'message': 'The request was successful!'
                },
                status=HTTP_200_OK
            )
        except Build.DoesNotExist:
            return Response(
                {
                    'error': 'invalid_build_id',
                    'message': 'A build with that ID does not exist!'
                },
                status=HTTP_404_NOT_FOUND
            )

    return Response(
        {
            'error': 'missing_parameters',
            'message': 'No parameters specified. Specify a file_name parameter or a build_id parameter.'
        },
        status=HTTP_400_BAD_REQUEST
    )


def build_increase_download_count(build):
    build.download_count += 1
    build.save()

    # Increase overall statistics
    try:
        stats = Statistics.objects.get(date=datetime.date.today())
    except Statistics.DoesNotExist:
        stats = Statistics.objects.create()

    stats.download_count += 1
    stats.save()


class ChunkedBuildUpload(ChunkedUploadView):
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
    return fields[2]    # Codename


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


def variant_check(variant):
    if variant not in ["gapps", "vanilla", "foss", "goapps"]:
        raise Http404("Wrong parameter. Try with the correct parameters.")


def v1_updater_los(request, codename, variant):
    """LOS-style endpoint used by updater app"""
    device = get_object_or_404(Device, codename=codename)

    variant_check(variant)

    if variant == "gapps":
        builds = device.get_all_gapps_build_objects()
    elif variant == "vanilla":
        builds = device.get_all_vanilla_build_objects()
    elif variant == "foss":
        builds = device.get_all_foss_build_objects()
    else:  # elif variant == "goapps":
        builds = device.get_all_goapps_build_objects()

    # Check if list is empty and return a 404
    if not builds:
        raise Http404("No builds exist for the specified variant yet!")

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
            "md5url": "https://" + request.get_host() + build.md5_file.url
        })

    return HttpResponse(json.dumps({"response": return_json}), content_type='application/json')


def v2_updater_device(request, codename, variant):
    """Updater endpoint used by the R updater"""
    device = get_object_or_404(Device, codename=codename)

    variant_check(variant)

    try:
        if variant == "gapps":
            build = device.get_latest_gapps_build_object()
        elif variant == "vanilla":
            build = device.get_latest_vanilla_build_object()
        elif variant == "foss":
            build = device.get_latest_foss_build_object()
        else:  # elif variant == "goapps":
            build = device.get_latest_goapps_build_object()
    except Build.DoesNotExist:
        raise Http404("No builds exist for the specified variant yet!")

    _, version, _, _, _, date = build.file_name.split('-')

    date = parse_build_date(date)

    return_json = {
        "date": int(date.strftime("%s")),
        "file_name": "{}.zip".format(build.file_name),
        "sha256": build.sha256sum,
        "size": build.size,
        "version": build.version,
        "zip_download_url": "https://" + request.get_host() + build.zip_file.url,
        "md5_download_url": "https://" + request.get_host() + build.md5_file.url
    }

    return HttpResponse(json.dumps(return_json), content_type='application/json')


def v2_all_builds(request):
    """Giant JSON response of ALL the builds in shipper"""
    return_json = {}

    for device in Device.objects.all():
        # Construct initial device JSON
        device_json = {
            "manufacturer": device.manufacturer,
            "name": device.name,
            "status": device.status,
            "photo": device.get_photo_url(),
            "builds": [],
        }

        # List builds for given device
        builds = device.get_all_build_objects()

        if not builds:
            continue

        for build in builds:
            _, version, _, _, _, date = build.file_name.split('-')

            date = parse_build_date(date)

            scheme = request.is_secure() and "https" or "http"

            build_json = {
                "date": int(date.strftime("%s")),
                "size": build.size,
                "version": build.version,
                "variant": build.variant,
                "mirror_list_page": "{}://{}/download/{}/{}/".format(scheme, request.get_host(), device.codename,
                                                                     build.id)
            }

            device_json["builds"].append(build_json)

        return_json[device.codename] = device_json

    return HttpResponse(json.dumps(return_json), content_type='application/json')


def parse_build_date(date):
    year = int(date[:4])
    month = int(date[4:-2])
    day = int(date[6:])

    return datetime.date(year, month, day)
