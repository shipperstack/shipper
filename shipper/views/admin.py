import humanize

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from shipper.models import Device, Build

User = get_user_model()


def get_total_size(build_list):
    total_size = 0
    for build in build_list:
        total_size += build.size

    return total_size


class AdminStatisticsView(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'admin_stats.html'

    def get(self, request, *args, **kwargs):
        devices = Device.objects.all()
        maintainers = User.objects.all()
        builds = Build.objects.all()
        vanilla_builds = builds.filter(variant="vanilla")
        gapps_builds = builds.filter(variant="gapps")
        foss_builds = builds.filter(variant="foss")
        goapps_builds = builds.filter(variant="goapps")
        builds_size = get_total_size(builds)
        vanilla_builds_size = get_total_size(vanilla_builds)
        gapps_builds_size = get_total_size(gapps_builds)
        foss_builds_size = get_total_size(foss_builds)
        goapps_builds_size = get_total_size(goapps_builds)

        data = {
            'enabled_devices_count': devices.filter(status=True).count(),
            'active_maintainers_count': maintainers.filter(is_active=True).count(),
            'disabled_devices_count': devices.filter(status=False).count(),
            'inactive_maintainers_count': maintainers.filter(is_active=False).count(),
            'builds_count': builds.count(),
            'vanilla_builds_count': vanilla_builds.count(),
            'gapps_builds_count': gapps_builds.count(),
            'foss_builds_count': foss_builds.count(),
            'goapps_builds_count': goapps_builds.count(),
            'builds_size': humanize.naturalsize(builds_size),
            'vanilla_builds_size': humanize.naturalsize(vanilla_builds_size),
            'gapps_builds_size': humanize.naturalsize(gapps_builds_size),
            'foss_builds_size': humanize.naturalsize(foss_builds_size),
            'goapps_builds_size': humanize.naturalsize(goapps_builds_size)
        }

        return render(request, self.template_name, data)
