from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from shipper.models import Device

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_active', 'email', 'last_login', 'get_devices', 'is_staff', 'is_superuser']
    ordering = ['-is_active', '-last_login']

    def get_devices(self, obj):
        return [device.codename for device in Device.objects.filter(maintainers=obj)]

    get_devices.short_description = 'Devices'


admin.site.register(User, CustomUserAdmin)
