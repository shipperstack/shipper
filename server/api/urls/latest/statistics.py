from django.urls import path

from api.views import (
    V2DownloadBuildCounter,
    v1_download_count_day,
    v1_download_count_week,
    v1_download_count_month,
    v1_download_count_all,
)

urlpatterns = [
    path(
        "download/build/counter/",
        V2DownloadBuildCounter.as_view(),
        name="latest_download_build_counter",
    ),
    path(
        "download/count/day/",
        v1_download_count_day,
        name="latest_download_count_day",
    ),
    path(
        "download/count/week/",
        v1_download_count_week,
        name="latest_download_count_week",
    ),
    path(
        "download/count/month/",
        v1_download_count_month,
        name="latest_download_count_month",
    ),
    path(
        "download/count/all/",
        v1_download_count_all,
        name="latest_download_count_all",
    ),
]
