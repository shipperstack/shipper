from django.urls import path

from api.views import v2_system_info

urlpatterns = [
    path("system/info/", v2_system_info, name="v2_system_info"),
]
