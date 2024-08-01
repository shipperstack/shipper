from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, ListView
from core.models import Build, Device


User = get_user_model()


class MaintainerDashboardView(LoginRequiredMixin, ListView):
    template_name = "maintainer_dashboard.html"
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return get_filtered_device_queryset(self.request.user).order_by(
            "-status", "manufacturer", "name"
        )


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = "device_detail.html"
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return get_filtered_device_queryset(self.request.user)


class BuildDeleteView(LoginRequiredMixin, DeleteView):
    model = Build
    template_name = "build_delete.html"

    def get_success_url(self):
        return reverse("device_detail", kwargs={"pk": self.get_object().device.id})

    # Override builds shown to maintainers
    def get_queryset(self):
        return get_filtered_build_queryset(self.request.user)


@login_required
def build_enabled_status_modify(request, pk):
    build = get_object_or_404(Build, pk=pk)

    # Check if maintainer is in device's approved maintainers list
    if not check_user_device_permission(request.user, build.device):
        raise PermissionDenied

    # Switch build status
    build.enabled = not build.enabled
    build.save()

    return redirect(reverse("device_detail", kwargs={"pk": build.device.id}))


def get_filtered_device_queryset(user: User) -> QuerySet:
    if user.full_access_to_devices:
        return Device.objects.all()
    else:
        return Device.objects.filter(maintainers=user)


def get_filtered_build_queryset(user: User) -> QuerySet:
    if user.full_access_to_devices:
        return Build.objects.all()
    else:
        return Build.objects.filter(device__maintainers=user)


def check_user_device_permission(user: User, device):
    if user.full_access_to_devices:
        return True

    if user in device.maintainers.all():
        return True

    return False
