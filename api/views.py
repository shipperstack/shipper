import json

from django.http import HttpResponse, Http404

from django.shortcuts import render, get_object_or_404
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


