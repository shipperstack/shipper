import json

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_chunked_upload.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from shipper.models import *


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
