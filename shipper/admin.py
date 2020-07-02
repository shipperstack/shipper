from django.contrib import admin

from .models import *


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'codename', 'manufacturer', 'status', 'created']
    search_fields = ['name', 'codename', 'manufacturer']
    ordering = ['-created']


class BuildAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'get_device_name', 'size', 'version']
    ordering = ['-created']

    def get_device_name(self, obj):
        return str(obj.device)
    get_device_name.short_description = 'Device'
    get_device_name.admin_order_field = 'device_name'


admin.site.register(Device, DeviceAdmin)
admin.site.register(Build, BuildAdmin)

