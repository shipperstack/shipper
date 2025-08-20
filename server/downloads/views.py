import os
import time

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.shortcuts import render
from core.models import Build, Device

from constance import config


class DownloadsMainView(TemplateView):
    template_name = "downloads_main.html"

    def get_context_data(self, **kwargs):
        active_visible_devices = [
            device
            for device in Device.objects.all()
            if device.has_enabled_hashed_builds() and device.visible
        ]
        return {
            "active_visible_devices": [
                {
                    "codename": device.codename,
                    "enabled": device.status,
                    "photo_url": device.photo_url,
                    "photo_thumbhash": device.photo_thumbhash,
                    "name": str(device),
                    "url": reverse(
                        "downloads_device", kwargs={"codename": device.codename}
                    ),
                }
                for device in active_visible_devices
            ]
        }


class DownloadsDeviceView(DetailView):
    template_name = "downloads_device.html"
    model = Device

    def get_object(self, queryset=None):
        return get_object_or_404(Device, codename=self.kwargs.get("codename"))


class DownloadsBuildView(DetailView):
    template_name = "downloads_build.html"
    model = Build


class LanguageSwitchView(TemplateView):
    template_name = "language_switch.html"

    def get(self, request, *args, **kwargs):
        redirect_url = request.GET.get("next", None)
        if not redirect_url:
            redirect_url = request.META.get("HTTP_REFERER", None)
        if not redirect_url:
            redirect_url = "/"
        return render(request, self.template_name, {"redirect_to": redirect_url})


def download_check_view(request, codename, file_name):
    build = get_object_or_404(Build, file_name=file_name, device__codename=codename)

    response = HttpResponse()

    if build.zip_file.name:
        response["X-Accel-Redirect"] = f"/internal/media/{build.zip_file.name}"
        response["Last-Modified"] = time.strftime(
            "%a,%e %b %Y %H:%M:%S %Z",
            time.gmtime(os.path.getmtime(build.zip_file.path)),
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{build.zip_file_basename()}"'
        )
        response["Content-Type"] = "application/octet-stream"

        if build.is_archived:
            limit_speed = config.SHIPPER_DOWNLOADS_ARCHIVE_THROTTLE * 1000 * 1000
            response["X-Accel-Limit-Rate"] = str(limit_speed)
        else:
            response["X-Accel-Limit-Rate"] = "off"
    else:
        response.status_code = 503
        response.content = """
The file is currently not available on the main server. Consider using one of
the mirror servers if there are any available."""

    return response
