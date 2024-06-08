from django.urls import path, include

urlpatterns = [
    path("", include("api.urls.latest.general")),
    path("", include("api.urls.latest.shippy")),
    path("", include("api.urls.latest.statistics")),
    path("", include("api.urls.latest.updater")),
]
