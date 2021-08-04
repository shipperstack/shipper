from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from shipper.models import Device, Build


class DownloadsMainView(ListView):
    template_name = 'downloads_main.html'
    model = Device

    ordering = ['-status', 'manufacturer', 'name']


class DownloadsDeviceView(DetailView):
    template_name = 'downloads_device.html'
    model = Device

    def get_object(self, queryset=None):
        return get_object_or_404(Device, codename=self.kwargs.get("codename"))


class DownloadsBuildView(DetailView):
    template_name = 'downloads_build.html'
    model = Build
