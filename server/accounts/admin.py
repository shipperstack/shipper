from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import Device

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "is_active",
        "get_full_name",
        "email",
        "last_login",
        "get_devices",
        "is_staff",
        "is_superuser",
        "full_access_to_devices",
    ]
    ordering = ["-is_active", "-last_login"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "profile_picture",
                    "bio",
                    "contact_url",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "full_access_to_devices",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)

    get_full_name.short_description = "Full Name"

    def get_devices(self, obj):
        return [device.codename for device in Device.objects.filter(maintainers=obj)]

    get_devices.short_description = "Devices"


admin.site.register(User, CustomUserAdmin)
