from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import *
from .forms import *
from .tasks import *
from .handler import *


class DownloadsView(ListView):
    template_name = 'shipper/downloads.html'
    model = Device

    def get(self, request, *args, **kwargs):
        self.extra_context = {'sourceforge_project_name': settings.SOURCEFORGE_PROJECT}
        return super().get(request, *args, **kwargs)


class MaintainerDashboardView(LoginRequiredMixin, ListView):
    template_name = 'shipper/maintainer_dashboard.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/device_detail.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class BuildDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/build_detail.html'
    model = Build

    # Override builds shown to maintainers
    def get_queryset(self):
        return Build.objects.filter(device__maintainers=self.request.user)


class BuildDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'shipper/build_delete.html'
    model = Build

    def get_success_url(self):
        return reverse('device_detail', kwargs={'pk': self.get_object().device.id})

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        codename = self.get_object().device.codename
        file_name = self.get_object().file_name
        delete_build.delay(codename, file_name)
        return HttpResponseRedirect(success_url)

    # Override builds shown to maintainers
    def get_queryset(self):
        return Build.objects.filter(device__maintainers=self.request.user)


@user_passes_test(lambda u: u.is_superuser)
def device_force_processing(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        process_build.delay(device.codename)
        return render(request, 'shipper/device_force_processing.html', {
            'device': device,
            'started': True,
        })

    return render(request, 'shipper/device_force_processing.html', {
        'device': device
    })


@login_required
def build_upload(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.user not in device.maintainers.all():
        raise Http404

    if request.method == 'POST':
        form = BuildUploadForm(request.POST, request.FILES)
        if form.is_valid():
            build_file = request.FILES['build_file']
            checksum_file = request.FILES['checksum_file']
            gapps = form.cleaned_data['gapps']
            release = form.cleaned_data['release']

            try:
                handle_builds(device, build_file, checksum_file, gapps, release)
            except Exception as e:
                return render(request, 'shipper/build_upload.html', {
                    'upload_succeeded': False,
                    'error_reason': e.args[0],
                    'device': device
                })

            return render(request, 'shipper/build_upload.html', {
                'upload_succeeded': True,
                'device': device
            })
        else:
            return render(request, 'shipper/build_upload.html', {
                'upload_succeeded': False,
                'error_reason': 'invalid_form',
                'device': device
            })
    else:
        form = BuildUploadForm()
    return render(request, 'shipper/build_upload.html', {
        'form': form,
        'device': device
    })
