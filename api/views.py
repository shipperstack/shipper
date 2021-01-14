import json

from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from shipper.models import *


def v2_updater_device(request, codename, gapps):
    device = get_object_or_404(Device, codename=codename)

    if gapps == "gapps":
        try:
            build = device.get_latest_gapps_build_object()
        except Build.DoesNotExist:
            raise Http404("No GApps builds exist for this device yet!")

    if gapps == "vanilla":
        try:
            build = device.get_latest_nongapps_build_object()
        except Build.DoesNotExist:
            raise Http404("No non-GApps builds exist for this device yet!")

    _, version, codename, build_type, gapps_raw, date = build.file_name.split('-')

    # Convert date into UNIX time
    year = int(date[:4])
    month = int(date[4:-2])
    day = int(date[6:])

    import datetime
    date = datetime.date(year, month, day)

    return_json = {
        "date": int(date.strftime("%s")),
        "file_name": "{}.zip".format(build.file_name),
        "sha256": build.sha256sum,
        "size": build.size,
        "version": build.version,
        "zip_download_url": request.get_host() + build.zip_file.url,
        "md5_download_url": request.get_host() + build.md5_file.url
    }

    return HttpResponse(json.dumps(return_json), content_type='application/json')


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

    retJson = {}

    for device in devices:
        maintainerJson = []
        for maintainer in device.maintainers.all():
            maintainerJson.append(maintainer.username)
        deviceJson = {
            "name": device.name,
            "cpu": device.CPU,
            "gpu": device.GPU,
            "manufacturer": device.manufacturer,
            "storage": device.storage,
            "memory": device.memory,
            "photo": device.photo,
            "maintainers": maintainerJson,
        }
        retJson[device.codename] = deviceJson

    return Response(
        retJson,
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
    cpu = request.data.get("cpu")
    gpu = request.data.get("gpu")
    manufacturer = request.data.get("manufacturer")
    storage = int(request.data.get("storage"))
    memory = int(request.data.get("memory"))
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
    new_device.CPU = cpu
    new_device.GPU = gpu
    new_device.manufacturer = manufacturer
    new_device.storage = storage
    new_device.memory = memory
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

    retJson = []

    for device in devices:
        for maintainer in device.maintainers.all():
            if maintainer.username not in retJson:
                retJson.append(maintainer.username)

    return Response(
        retJson,
        status=HTTP_200_OK
    )