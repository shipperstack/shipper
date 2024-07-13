from django.urls import path

from api.views import (
    V1GeneralDeviceAll,
    V1GeneralMaintainerAll,
    V1GeneralMaintainerActive,
    V1GeneralBuildLatest,
    v1_general_build_magic_download,
)

urlpatterns = [
    path(
        "general/device/all/",
        V1GeneralDeviceAll.as_view(),
        name="latest_general_device_all",
    ),
    path(
        "general/maintainer/all/",
        V1GeneralMaintainerAll.as_view(),
        name="latest_general_maintainer_all",
    ),
    path(
        "general/maintainer/active/",
        V1GeneralMaintainerActive.as_view(),
        name="latest_general_maintainer_active",
    ),
    path(
        "general/build/latest/<slug:codename>/<slug:variant>/",
        V1GeneralBuildLatest.as_view(),
        name="latest_general_build_latest",
    ),
    path(
        "general/build/magic_download/<slug:codename>/<slug:file_name>/",
        v1_general_build_magic_download,
        name="latest_general_build_magic_download",
    ),
]
