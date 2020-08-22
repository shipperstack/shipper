import json

from django.http import HttpResponse, Http404

from django.shortcuts import render, get_object_or_404
from shipper.models import *


def v1_updater(request):
    retJson = {}
    for device in Device.objects.all():
        try:
            build = device.get_latest_build_object()
        except Build.DoesNotExist:
            continue
        _, version, codename, type, date = build.file_name.split('-')

        deviceJson = {
            "date": date,
            "filename": "{}.zip".format(build.file_name),
            "download_url": "https://sourceforge.net/projects/{}/files/Q/{}/{}/download".format(
                settings.SOURCEFORGE_PROJECT,
                device.codename,
                "{}.zip".format(build.file_name)
            ),
            "sha256": build.sha256sum,
            "size": build.size,
            "type": "official",
            "version": build.version
        }

        retJson[codename] = [deviceJson]
    return HttpResponse(json.dumps(retJson), content_type='application/json')

def v1_updater_device(request, codename, release):

    # Check if device exists
    device = get_object_or_404(Device, codename=codename)

    try:
        build = device.get_latest_build_object()
    except Build.DoesNotExist:
        raise Http404("No builds exist for this device yet!")
    _, version, codename, type, date = build.file_name.split('-')

    # Convert date into UNIX time
    year = int(date[:4])
    month = int(date[4:-2])
    day = int(date[6])

    import datetime
    date = datetime.date(year, month, day)

    """
    Yes this is a horrifying JSON structure but the legacy system requires it.
    """
    retJson = {
        "response": [
                {
                    "datetime": int(date.strftime("%s")),
                    "filename": "{}.zip".format(build.file_name),
                    "id": build.sha256sum,
                    "romtype": "official",
                    "size": build.size,
                    "url": "https://sourceforge.net/projects/{}/files/Q/{}/{}/download".format(
                               settings.SOURCEFORGE_PROJECT,
                               device.codename,
                               "{}.zip".format(build.file_name)
                    ),
                    "version": build.version,
                }
        ]
    }

    return HttpResponse(json.dumps(retJson), content_type='application/json')
