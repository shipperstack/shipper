from django.urls import path
from rest_framework.schemas import get_schema_view

from config import settings
from .views import (
    V1GeneralBuildLatest,
    V1GeneralDeviceAll,
    V1GeneralMaintainerAll,
    V1GeneralMaintainerActive,
    V1MaintainersChunkedUpload,
    V1UpdaterLOS,
    v1_download_count_all,
    v1_download_count_day,
    v1_download_count_month,
    v1_download_count_week,
    v1_maintainers_build_enabled_status_modify,
    v1_maintainers_login,
    v1_maintainers_token_check,
    v1_maintainers_upload_filename_regex_pattern,
    v1_system_info,
    V2DownloadBuildCounter,
    v2_system_info,
)

urlpatterns = [
    # OpenAPI schema
    path(
        "openapi/",
        get_schema_view(
            title="shipper", description="shipper API", version=settings.SHIPPER_VERSION
        ),
        name="openapi-schema",
    ),
    # statistics
    path(
        "latest/download/build/counter/",
        V2DownloadBuildCounter.as_view(),
        name="latest_download_build_counter",
    ),
    path(
        "latest/download/count/day/",
        v1_download_count_day,
        name="latest_download_count_day",
    ),
    path(
        "latest/download/count/week/",
        v1_download_count_week,
        name="latest_download_count_week",
    ),
    path(
        "latest/download/count/month/",
        v1_download_count_month,
        name="latest_download_count_month",
    ),
    path(
        "latest/download/count/all/",
        v1_download_count_all,
        name="latest_download_count_all",
    ),
    path(
        "v2/download/build/counter/",
        V2DownloadBuildCounter.as_view(),
        name="v2_download_build_counter",
    ),
    path("v1/download/count/day/", v1_download_count_day, name="v1_download_count_day"),
    path(
        "v1/download/count/week/", v1_download_count_week, name="v1_download_count_week"
    ),
    path(
        "v1/download/count/month/",
        v1_download_count_month,
        name="v1_download_count_month",
    ),
    path("v1/download/count/all/", v1_download_count_all, name="v1_download_count_all"),
    # shippy
    path("latest/system/info/", v2_system_info, name="latest_system_info"),
    path(
        "latest/maintainers/login/",
        v1_maintainers_login,
        name="latest_maintainers_login",
    ),
    path(
        "latest/maintainers/token_check/",
        v1_maintainers_token_check,
        name="latest_maintainers_token_check",
    ),
    path(
        "latest/maintainers/upload_filename_regex_pattern",
        v1_maintainers_upload_filename_regex_pattern,
        name="latest_maintainers_upload_filename_regex_pattern",
    ),
    path(
        "latest/maintainers/chunked_upload/",
        V1MaintainersChunkedUpload.as_view(),
        name="latest_maintainers_chunked_upload",
    ),
    path(
        "latest/maintainers/chunked_upload/<uuid:pk>/",
        V1MaintainersChunkedUpload.as_view(),
        name="latest_maintainers_chunked_upload_detail",
    ),
    path(
        "latest/maintainers/build/enabled_status_modify/",
        v1_maintainers_build_enabled_status_modify,
        name="latest_maintainers_build_enabled_status_modify",
    ),
    path("v2/system/info/", v2_system_info, name="v2_system_info"),
    path("v1/system/info/", v1_system_info, name="v1_system_info"),
    path("v1/maintainers/login/", v1_maintainers_login, name="v1_maintainers_login"),
    path(
        "v1/maintainers/token_check/",
        v1_maintainers_token_check,
        name="v1_maintainers_token_check",
    ),
    path(
        "v1/maintainers/upload_filename_regex_pattern",
        v1_maintainers_upload_filename_regex_pattern,
        name="v1_maintainers_upload_filename_regex_pattern",
    ),
    path(
        "v1/maintainers/chunked_upload/",
        V1MaintainersChunkedUpload.as_view(),
        name="v1_maintainers_chunked_upload",
    ),
    path(
        "v1/maintainers/chunked_upload/<uuid:pk>/",
        V1MaintainersChunkedUpload.as_view(),
        name="v1_maintainers_chunked_upload_detail",
    ),
    path(
        "v1/maintainers/build/enabled_status_modify/",
        v1_maintainers_build_enabled_status_modify,
        name="v1_maintainers_build_enabled_status_modify",
    ),
    # updater
    path(
        "latest/updater/los/<slug:codename>/<slug:variant>/",
        V1UpdaterLOS.as_view(),
        name="latest_updater_los",
    ),
    path(
        "v1/updater/los/<slug:codename>/<slug:variant>/",
        V1UpdaterLOS.as_view(),
        name="v1_updater_los",
    ),
    # general
    path(
        "latest/general/device/all/",
        V1GeneralDeviceAll.as_view(),
        name="latest_general_device_all",
    ),
    path(
        "latest/general/maintainer/all/",
        V1GeneralMaintainerAll.as_view(),
        name="latest_general_maintainer_all",
    ),
    path(
        "latest/general/maintainer/active/",
        V1GeneralMaintainerActive.as_view(),
        name="latest_general_maintainer_active",
    ),
    path(
        "latest/general/build/latest/<slug:codename>/<slug:variant>/",
        V1GeneralBuildLatest.as_view(),
        name="latest_general_build_latest",
    ),
    path(
        "v1/general/device/all/",
        V1GeneralDeviceAll.as_view(),
        name="v1_general_device_all",
    ),
    path(
        "v1/general/maintainer/all/",
        V1GeneralMaintainerAll.as_view(),
        name="v1_general_maintainer_all",
    ),
    path(
        "v1/general/maintainer/active/",
        V1GeneralMaintainerActive.as_view(),
        name="v1_general_maintainer_active",
    ),
    path(
        "v1/general/build/latest/<slug:codename>/<slug:variant>/",
        V1GeneralBuildLatest.as_view(),
        name="v1_general_build_latest",
    ),
]
