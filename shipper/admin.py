from django.contrib import admin

from .models import Device, Build, MirrorServer, Statistics


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'manufacturer', 'name', 'codename', 'get_maintainers', 'status', 'created']
    list_filter = ['status']
    search_fields = ['name', 'codename', 'manufacturer']
    ordering = ['-status', 'manufacturer', 'name']

    def get_maintainers(self, obj):
        return ",".join([maintainer.username for maintainer in obj.maintainers.all()])

    get_maintainers.short_description = 'Maintainers'


class BuildAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'file_name', 'get_device_name', 'get_human_readable_size', 'version', 'variant',
                    'get_build_device_maintainers', 'download_count', 'is_processed', 'is_backed_up', 'created']
    list_filter = ['enabled']
    ordering = ['-created']

    def is_processed(self, obj):
        return obj.sha256sum != ''

    is_processed.short_description = 'Processed'
    is_processed.boolean = True

    def is_backed_up(self, obj):
        # Check if all mirrors are disabled
        if MirrorServer.objects.filter(enabled=True).count() == 0:
            return False

        return all(mirror in obj.mirrored_on.all() for mirror in list(MirrorServer.objects.filter(enabled=True)))

    is_backed_up.short_description = 'Backed Up'
    is_backed_up.boolean = True

    def get_device_name(self, obj):
        return str(obj.device)

    get_device_name.short_description = 'Device'
    get_device_name.admin_order_field = 'device_name'

    def get_build_device_maintainers(self, obj):
        return ",".join([maintainer.username for maintainer in obj.device.maintainers.all()])

    get_build_device_maintainers.short_description = 'Maintainers'

    def get_human_readable_size(self, obj):
        return obj.get_human_readable_size()

    get_human_readable_size.short_description = 'Size'


class MirrorServerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'hostname', 'enabled', 'downloadable']
    list_filter = ['enabled', 'downloadable']
    ordering = ['-enabled', '-downloadable']


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'download_count']
    ordering = ['-date']


admin.site.register(Device, DeviceAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(MirrorServer, MirrorServerAdmin)
admin.site.register(Statistics, StatisticsAdmin)
