import humanize

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from shipper.models import Device, Build

User = get_user_model()


def get_humanized_total_size(build_list):
    total_size = 0
    for build in build_list:
        total_size += build.size

    return humanize.naturalsize(total_size)


class AdminStatisticsView(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'admin_stats.html'

    def get(self, request, *args, **kwargs):
        devices = Device.objects.all()
        maintainers = User.objects.all()
        builds = Build.objects.all()

        data = {
            'enabled_devices_count': devices.filter(status=True).count(),
            'active_maintainers_count': maintainers.filter(is_active=True).count(),
            'disabled_devices_count': devices.filter(status=False).count(),
            'inactive_maintainers_count': maintainers.filter(is_active=False).count(),
            'builds_count': builds.count(),
            'builds_size': get_humanized_total_size(builds),
        }

        return render(request, self.template_name, data)
