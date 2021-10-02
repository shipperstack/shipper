from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView

from shipper.exceptions import UploadException
from shipper.forms import BuildUploadForm
from shipper.handler import handle_build
from shipper.models import Device, Build


class MaintainerDashboardView(LoginRequiredMixin, ListView):
    template_name = 'maintainer_dashboard.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user).order_by('-status', 'manufacturer', 'name')


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'device_detail.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class BuildDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'build_delete.html'
    model = Build

    def get_success_url(self):
        return reverse('device_detail', kwargs={'pk': self.get_object().device.id})

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.get_object().delete()
        return HttpResponseRedirect(success_url)

    # Override builds shown to maintainers
    def get_queryset(self):
        return Build.objects.filter(device__maintainers=self.request.user)


@login_required
def build_enabled_status_modify(request, pk):
    build = get_object_or_404(Build, pk=pk)

    # Check if maintainer is in device's approved maintainers list
    if request.user not in build.device.maintainers.all():
        raise Http404

    # Switch build status
    build.enabled = not build.enabled
    build.save()

    return redirect(reverse('device_detail', kwargs={'pk': build.device.id}))


@login_required
def build_upload(request, pk):
    device = get_object_or_404(Device, pk=pk)

    # Check if maintainer is in device's approved maintainers list
    if request.user not in device.maintainers.all():
        raise Http404

    if request.method == 'POST':
        form = BuildUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                build_id = handle_build(device, request.FILES["zip_file"], request.FILES["md5_file"])
            # TODO: add status code
            except UploadException as exception:
                return render(request, 'build_upload.html', {
                    'upload_succeeded': False,
                    'error_reason': str(exception),
                    'device': device,
                    'form': form
                })

            # TODO: add status code
            return render(request, 'build_upload.html', {
                'upload_succeeded': True,
                'device': device,
                'form': form,
                'build_id': build_id
            })

        # TODO: add status code
        return render(request, 'build_upload.html', {
            'upload_succeeded': False,
            'error_reason': 'invalid_form',
            'device': device,
            'form': form
        })

    form = BuildUploadForm()
    # TODO: add status code
    return render(request, 'build_upload.html', {
        'form': form,
        'device': device
    })
