from django.urls import path

from api.views import V1UpdaterLOS, V1UpdaterLOSX86

urlpatterns = [
    path(
        "updater/los/<slug:codename>/<slug:variant>/",
        V1UpdaterLOS.as_view(),
        name="latest_updater_los",
    ),
    path(
        "updater/los/<slug:codename>/<slug:x86_type>/<slug:variant>/",
        V1UpdaterLOSX86.as_view(),
        name="latest_updater_los_x86",
    ),
]
