from django.contrib import admin

from .models import *


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'codename', 'created']


admin.site.register(Device, DeviceAdmin)

