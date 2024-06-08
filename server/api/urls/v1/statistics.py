from django.urls import path

from api.views import (
    v1_download_count_day,
    v1_download_count_week,
    v1_download_count_month,
    v1_download_count_all,
)

urlpatterns = [
    path("download/count/day/", v1_download_count_day, name="v1_download_count_day"),
    path("download/count/week/", v1_download_count_week, name="v1_download_count_week"),
    path(
        "download/count/month/",
        v1_download_count_month,
        name="v1_download_count_month",
    ),
    path("download/count/all/", v1_download_count_all, name="v1_download_count_all"),
]
