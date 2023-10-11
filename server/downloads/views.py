from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import render
from core.models import Build, Device

from constance import config


class DownloadsMainView(TemplateView):
    template_name = "downloads_main.html"

    def get_context_data(self, **kwargs):
        active_devices = [
            device
            for device in Device.objects.all()
            if device.has_enabled_hashed_builds()
        ]
        return {
            "active_devices": [
                {
                    "codename": device.codename,
                    "enabled": device.status,
                    "photo_url": device.photo_url,
                    "name": str(device),
                    "url": reverse(
                        "downloads_device", kwargs={"codename": device.codename}
                    ),
                }
                for device in active_devices
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


def download_view(request, codename, file_name):
    build = get_object_or_404(Build, file_name=file_name, device__codename=codename)
    response = HttpResponse()
    response["X-Accel-Redirect"] = f"/media/{codename}/{file_name}"

    if build.is_archived:
        limit_speed = config.SHIPPER_DOWNLOADS_ARCHIVE_THROTTLE * 1000
        response["X-Accel-Limit-Rate"] = str(limit_speed)

    return response
