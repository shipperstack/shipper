from django.urls import path

from .views import (
    V1DownloadBuildCounter,
    V1GeneralBuildLatest,
    V1GeneralDeviceAll,
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
)

urlpatterns = [
    # statistics
    path(
        "v1/download/build/counter/",
        V1DownloadBuildCounter.as_view(),
        name="v1_download_build_counter",
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
        "v1/updater/los/<slug:codename>/<slug:variant>/",
        V1UpdaterLOS.as_view(),
        name="v1_updater_los",
    ),
    # general
    path(
        "v1/general/device/all/",
        V1GeneralDeviceAll.as_view(),
        name="v1_general_device_all",
    ),
    path(
        "v1/general/build/latest/<slug:codename>/<slug:variant>/",
        V1GeneralBuildLatest.as_view(),
        name="v1_general_build_latest",
    ),
]
