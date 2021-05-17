import json
import datetime

from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from shipper.models import *


def v1_updater_los(request, codename, gapps):
    device = get_object_or_404(Device, codename=codename)

    if gapps == "gapps":
        builds = device.get_all_gapps_build_objects()
    elif gapps == "vanilla":
        builds = device.get_all_vanilla_build_objects()
    else:
        raise Http404("Wrong parameter. Try with the correct parameters.")

    # Check if list is empty and return a 404
    if not builds:
        if gapps == "gapps":
            raise Http404("No GApps builds exist for this device yet!")
        elif gapps == "vanilla":
            raise Http404("No non-GApps builds exist for this device yet!")

    return_json = []

    for build in builds:
        _, version, codename, build_type, gapps_raw, date = build.file_name.split('-')

        date = parse_build_date(date)

        return_json.append({
            "datetime": int(date.strftime("%s")),
            "filename": "{}.zip".format(build.file_name),
            "id": build.sha256sum,      # WHY
            "size": build.size,
            "version": build.version,
            "variant": gapps,
            "url": "https://" + request.get_host() + build.zip_file.url,
            "md5url": "https://" + request.get_host() + build.md5_file.url
        })

    return HttpResponse(json.dumps({"response": return_json}), content_type='application/json')


def v2_updater_device(request, codename, gapps):
    device = get_object_or_404(Device, codename=codename)

    if gapps == "gapps":
        try:
            build = device.get_latest_gapps_build_object()
        except Build.DoesNotExist:
            raise Http404("No GApps builds exist for this device yet!")
    elif gapps == "vanilla":
        try:
            build = device.get_latest_vanilla_build_object()
        except Build.DoesNotExist:
            raise Http404("No non-GApps builds exist for this device yet!")
    else:
        raise Http404("Wrong parameter. Try with the correct parameters.")

    _, version, codename, build_type, gapps_raw, date = build.file_name.split('-')

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


def parse_build_date(date):
    year = int(date[:4])
    month = int(date[4:-2])
    day = int(date[6:])

    return datetime.date(year, month, day)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_internal_device_list(request):
    internal_password = request.data.get("internal_password")

    devices = Device.objects.all()

    if internal_password != settings.SHIPPER_INTERNAL_PASSWORD:
        return Response(
            {
                'error': 'incorrect_password',
                'message': 'The internal password is incorrect!'
            },
            status=HTTP_401_UNAUTHORIZED
        )

    return_json = {}

    for device in devices:
        maintainer_json = []
        for maintainer in device.maintainers.all():
            maintainer_json.append(maintainer.username)
        device_json = {
            "name": device.name,
            "manufacturer": device.manufacturer,
            "photo": device.get_photo_url(),
            "maintainers": maintainer_json,
        }
        return_json[device.codename] = device_json

    return Response(
        return_json,
        status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def v1_internal_device_add(request):
    internal_password = request.data.get("internal_password")

    if internal_password != settings.SHIPPER_INTERNAL_PASSWORD:
        return Response(
            {
                'error': 'incorrect_password',
                'message': 'The internal password is incorrect!'
            },
            status=HTTP_401_UNAUTHORIZED
        )

    devices = Device.objects.all()

    name = request.data.get("name")
    codename = request.data.get("codename")
    manufacturer = request.data.get("manufacturer")
    photo = request.data.get("photo")

    # Check if device already exists
    for device in devices:
        if device.codename == codename:
            return Response(
                {
                    'error': 'device_exists',
                    'message': 'The specified device already exists!'
                },
                status=HTTP_400_BAD_REQUEST
            )

    new_device = Device(codename=codename)
    new_device.name = name
    new_device.manufacturer = manufacturer
    new_device.photo = photo

    new_device.save()

    return Response(
        {
            'message': 'The device was successfully added!'
        },
        status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_internal_maintainer_list(request):
    internal_password = request.data.get("internal_password")

    devices = Device.objects.all()

    if internal_password != settings.SHIPPER_INTERNAL_PASSWORD:
        return Response(
            {
                'error': 'incorrect_password',
                'message': 'The internal password is incorrect!'
            },
            status=HTTP_401_UNAUTHORIZED
        )

    return_json = []

    for device in devices:
        for maintainer in device.maintainers.all():
            if maintainer.username not in return_json:
                return_json.append(maintainer.username)

    return Response(
        return_json,
        status=HTTP_200_OK
    )
