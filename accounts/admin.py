from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from shipper.models import Device

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_active', 'get_full_name', 'email', 'last_login', 'get_devices', 'is_staff',
                    'is_superuser']
    ordering = ['-is_active', '-last_login']

    # noinspection PyMethodMayBeStatic
    def get_full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)

    def get_devices(self, obj):
        return [device.codename for device in Device.objects.filter(maintainers=obj)]

    get_devices.short_description = 'Devices'


admin.site.register(User, CustomUserAdmin)
