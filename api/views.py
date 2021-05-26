import json
import datetime

from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404

from shipper.models import *


def v1_updater_los(request, codename, variant):
    device = get_object_or_404(Device, codename=codename)

    if variant not in ["gapps", "vanilla", "foss", "goapps"]:
        raise Http404("Wrong parameter. Try with the correct parameters.")

    if variant == "gapps":
        builds = device.get_all_gapps_build_objects()
    elif variant == "vanilla":
        builds = device.get_all_vanilla_build_objects()
    elif variant == "foss":
        builds = device.get_all_foss_build_objects()
    elif variant == "goapps":
        builds = device.get_all_goapps_build_objects()
    else:
        builds = None

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
            "id": build.sha256sum,      # WHY
            "size": build.size,
            "version": build.version,
            "variant": variant,
            "url": "https://" + request.get_host() + build.zip_file.url,
            "md5url": "https://" + request.get_host() + build.md5_file.url
        })

    return HttpResponse(json.dumps({"response": return_json}), content_type='application/json')


def v2_updater_device(request, codename, variant):
    device = get_object_or_404(Device, codename=codename)

    if variant not in ["gapps", "vanilla", "foss", "goapps"]:
        raise Http404("Wrong parameter. Try with the correct parameters.")

    try:
        if variant == "gapps":
            build = device.get_latest_gapps_build_object()
        elif variant == "vanilla":
            build = device.get_latest_vanilla_build_object()
        elif variant == "foss":
            build = device.get_latest_foss_build_object()
        elif variant == "goapps":
            build = device.get_latest_goapps_build_object()
        else:
            build = None
    except Build.DoesNotExist:
        raise Http404("No builds exist for the specified variant yet!")

    # Check to make sure build isn't None
    if not build:
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


def parse_build_date(date):
    year = int(date[:4])
    month = int(date[4:-2])
    day = int(date[6:])

    return datetime.date(year, month, day)
