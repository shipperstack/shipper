from django.contrib import admin

from .models import *


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'codename', 'manufacturer', 'status', 'created']
    search_fields = ['name', 'codename', 'manufacturer']
    ordering = ['-created']


class VariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'device', 'created']
    search_fields = ['name', 'device']
    ordering = ['-created']


class BuildAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'variant', 'variant.device', 'size', 'version']
    ordering = ['-created']


admin.site.register(Device, DeviceAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Build, BuildAdmin)

