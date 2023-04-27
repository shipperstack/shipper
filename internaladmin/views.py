import json
import re

import humanize
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django_celery_results.models import TaskResult

from core.models import Build, Device

User = get_user_model()


def get_humanized_total_size(build_list):
    total_size = 0
    for build in build_list:
        total_size += build.size

    return humanize.naturalsize(total_size)


class AdminStatisticsView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_staff"
    template_name = "admin_stats.html"

    def get(self, request, *args, **kwargs):
        devices = Device.objects.all()
        maintainers = User.objects.all()
        builds = Build.objects.all()

        data = {
            "enabled_devices_count": devices.filter(status=True).count(),
            "active_maintainers_count": maintainers.filter(is_active=True).count(),
            "disabled_devices_count": devices.filter(status=False).count(),
            "inactive_maintainers_count": maintainers.filter(is_active=False).count(),
            "builds_count": builds.count(),
            "builds_size": get_humanized_total_size(builds),
        }

        return render(request, self.template_name, data)


class AdminBuildMirrorStatusView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_staff"
    template_name = "admin_build_mirror_status.html"

    def get(self, request, *args, **kwargs):
        fetch_limit = 100
        raw_results = TaskResult.objects.filter(task_name="mirror_build")[:fetch_limit]
        mirror_results = []

        for raw_result in raw_results:
            build_id = int(re.search(r'\d+', raw_result.task_args).group())
            build = Build.objects.get(id=build_id)

            upload_result = json.loads(raw_result.result)

            # Some tasks never record the current progress, so we need to check if the
            # JSON load was successful here
            if upload_result is None:
                current = 0
                total = 0
                percent = 0
            else:
                try:
                    current = upload_result["current"]
                except KeyError:
                    current = -1
                try:
                    total = upload_result["total"]
                except KeyError:
                    total = -1
                percent = int(current * 100 / total)

            mirror_results.append(
                {
                    "build_name": build.file_name,
                    "status": raw_result.status,
                    "current": humanize.naturalsize(current),
                    "total": humanize.naturalsize(total),
                    "percent": percent,
                }
            )

        data = {
            "mirror_results": mirror_results,
            "fetch_limit": fetch_limit,
        }

        return render(request, self.template_name, data)
