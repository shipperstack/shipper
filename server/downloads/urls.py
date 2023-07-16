from django.urls import path

from .views import (
    DownloadsBuildView,
    DownloadsDeviceView,
    DownloadsMainView,
    LanguageSwitchView,
)

urlpatterns = [
    path("", DownloadsMainView.as_view(), name="downloads"),
    path(
        "download/<slug:codename>/",
        DownloadsDeviceView.as_view(),
        name="downloads_device",
    ),
    path(
        "download/<slug:codename>/<int:pk>/",
        DownloadsBuildView.as_view(),
        name="downloads_build",
    ),
    path("language_switch/", LanguageSwitchView.as_view(), name="language_switch"),
]