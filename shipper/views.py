from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from .models import *
from .forms import *
from .tasks import process_build
from .utils import delete_artifact


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'shipper/dashboard.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/device_detail.html'
    model = Device


class BuildDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/build_detail.html'
    model = Build


def build_upload(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        form = BuildUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('build_file')
        if form.is_valid():
            gapps = form.cleaned_data['gapps']
            release = form.cleaned_data['release']
            for f in files:
                import os
                from pathlib import Path
                # Make sure path exists
                Path(os.path.join(settings.MEDIA_ROOT, device.codename)).mkdir(parents=True, exist_ok=True)
                with open(os.path.join(settings.MEDIA_ROOT, device.codename, f.name), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                file_name, file_extension = os.path.splitext(f.name)
                if file_extension == '.zip':
                    _, version, codename, type, date = file_name.split('-')
                    if codename != device.codename:
                        # Incorrect device uploaded
                        return render(request, 'shipper/build_upload.html', {
                            'upload_succeeded': False,
                            'invalid_form': True,
                            'device': device
                        })
                    if Build.objects.filter(file_name=file_name).count() >= 1:
                        # Build already exists
                        return render(request, 'shipper/build_upload.html', {
                            'upload_succeeded': False,
                            'device': device
                        })
                    build = Build(
                        device=device,
                        file_name=file_name,
                        size=f.size,
                        version=version,
                        sha256sum="0",
                        gapps=gapps,
                        release=release
                    )
                    build.save()
            process_build.delay(device.codename)
            return render(request, 'shipper/build_upload.html', {
                'upload_succeeded': True,
                'device': device
            })
        else:
            return render(request, 'shipper/build_upload.html', {
                'upload_succeeded': False,
                'invalid_form': True,
                'device': device
            })
    else:
        form = BuildUploadForm()
    return render(request, 'shipper/build_upload.html', {
        'form': form,
        'device': device
    })
