from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, ListView
from core.models import Build, Device


class MaintainerDashboardView(LoginRequiredMixin, ListView):
    template_name = "maintainer_dashboard.html"
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return get_filtered_device_queryset(self.request.user).order_by("-status", "manufacturer", "name")


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = "device_detail.html"
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return get_filtered_device_queryset(self.request.user)


class BuildDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "build_delete.html"
    model = Build

    def get_success_url(self):
        return reverse("device_detail", kwargs={"pk": self.get_object().device.id})

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.get_object().delete()
        return HttpResponseRedirect(success_url)

    # Override builds shown to maintainers
    def get_queryset(self):
        return get_filtered_device_queryset(self.request.user)


@login_required
def build_enabled_status_modify(request, pk):
    build = get_object_or_404(Build, pk=pk)

    # Check if maintainer is in device's approved maintainers list
    if request.user not in build.device.maintainers.all():
        raise PermissionDenied

    # Switch build status
    build.enabled = not build.enabled
    build.save()

    return redirect(reverse("device_detail", kwargs={"pk": build.device.id}))


def get_filtered_device_queryset(user):
    if user.full_access_to_devices:
        return Device.objects.all()
    else:
        return Device.objects.filter(maintainers=user)