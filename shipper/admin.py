from django.contrib import admin

from .models import *


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'manufacturer', 'name', 'codename', 'get_maintainers', 'status', 'created']
    search_fields = ['name', 'codename', 'manufacturer']
    ordering = ['-created']

    def get_maintainers(self, obj):
        return ",".join([maintainer.username for maintainer in obj.maintainers.all()])
    get_maintainers.short_description = 'Maintainers'

    # Override devices shown to maintainers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow superusers to modify any device
        if request.user.is_superuser:
            return qs
        return qs.filter(maintainers=request.user)


class BuildAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'get_device_name', 'size', 'version']
    ordering = ['-created']

    def get_device_name(self, obj):
        return str(obj.device)
    get_device_name.short_description = 'Device'
    get_device_name.admin_order_field = 'device_name'


admin.site.register(Device, DeviceAdmin)
admin.site.register(Build, BuildAdmin)

