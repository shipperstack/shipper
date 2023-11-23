from django.contrib import admin

from .custom_filters import BuildHashedFilter, BuildMirroredFilter, BuildArchivedFilter
from .models import Build, Device, Variant, MirrorServer, Statistics


class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "manufacturer",
        "name",
        "codename",
        "get_maintainers",
        "status",
        "created",
    ]
    list_filter = ["status"]
    search_fields = ["name", "codename", "manufacturer"]
    ordering = ["-status", "manufacturer", "name"]
    save_as = True

    @admin.display(description="Maintainers")
    def get_maintainers(self, obj):
        return ",".join([maintainer.username for maintainer in obj.maintainers.all()])


class BuildAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "enabled",
        "file_name",
        "get_device_name",
        "get_human_readable_size",
        "version",
        "variant",
        "get_build_device_maintainers",
        "get_download_count",
        "is_hashed",
        "is_archived",
        "is_mirrored",
        "created",
    ]
    list_filter = [
        "enabled",
        BuildHashedFilter,
        BuildMirroredFilter,
        BuildArchivedFilter,
    ]
    ordering = ["-created"]
    search_fields = ["id", "file_name"]

    @admin.display(
        description="Device",
        ordering="device_name",
    )
    def get_device_name(self, obj):
        return str(obj.device)

    @admin.display(description="Maintainers")
    def get_build_device_maintainers(self, obj):
        return ",".join(
            [maintainer.username for maintainer in obj.device.maintainers.all()]
        )

    @admin.display(description="Size")
    def get_human_readable_size(self, obj):
        return obj.get_human_readable_size()

    @admin.display(description="Download Count")
    def get_download_count(self, obj):
        return obj.get_download_count()


class VariantAdmin(admin.ModelAdmin):
    list_display = ["codename", "description"]
    ordering = ["codename"]
    save_as = True


class MirrorServerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "hostname", "enabled", "downloadable"]
    list_filter = ["enabled", "downloadable"]
    ordering = ["-enabled", "-downloadable"]
    save_as = True


class StatisticsAdmin(admin.ModelAdmin):
    readonly_fields = ["time", "build", "download_type", "ip"]
    list_display = ["time", "build", "download_type", "ip"]
    list_filter = ["download_type"]
    ordering = ["-time"]


admin.site.register(Device, DeviceAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(MirrorServer, MirrorServerAdmin)
admin.site.register(Statistics, StatisticsAdmin)
