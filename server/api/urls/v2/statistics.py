from django.urls import path

from api.views import V2DownloadBuildCounter

urlpatterns = [
    path(
        "download/build/counter/",
        V2DownloadBuildCounter.as_view(),
        name="v2_download_build_counter",
    ),
]
