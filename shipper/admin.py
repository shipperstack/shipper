from django.contrib import admin

from .models import *


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'codename', 'manufacturer', 'status', 'created']
    search_fields = ['name', 'codename', 'manufacturer']
    ordering = ['-created']


admin.site.register(Device, DeviceAdmin)

