import json

from django.http import HttpResponse

from django.shortcuts import render
from shipper.models import *


def v1_updater(request):
    retJson = {}
    for device in Device.objects.all():
        build = device.get_latest_build_object()
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
