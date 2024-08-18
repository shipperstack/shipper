import json
import re

import humanize
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django_celery_results.models import TaskResult

from core.models import Build, Device

User = get_user_model()


def get_humanized_total_size(build_list):
    total_size = 0
    for build in build_list:
        total_size += build.size

    return humanize.naturalsize(total_size)


@method_decorator(cache_page(0), name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class AdminStatisticsView(TemplateView):
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


@method_decorator(cache_page(0), name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class AdminBuildMirrorStatusView(TemplateView):
    template_name = "admin_build_mirror_status.html"

    def get(self, request, *args, **kwargs):
        fetch_limit = 100
        raw_results = TaskResult.objects.filter(task_name="mirror_build")[:fetch_limit]
        mirror_results = []

        for raw_result in raw_results:
            build_id = int(re.search(r"\d+", raw_result.task_args).group())
            try:
                build = Build.objects.get(id=build_id)
            except Build.DoesNotExist:
                continue

            upload_result = json.loads(raw_result.result)

            def load_values_or_default(result, key, default=0):
                if result is None or key not in result:
                    return default
                else:
                    return result[key]

            current = load_values_or_default(upload_result, "current", -1)
            total = load_values_or_default(upload_result, "total", -1)

            if upload_result is None:
                if raw_result.status == "SUCCESS":
                    percent = 100
                else:
                    percent = 0
            else:
                percent = int(current * 100 / total)

            mirror_results.append(
                {
                    "task_id": raw_result.id,
                    "created_on": raw_result.date_created,
                    "last_updated": raw_result.date_done,
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
