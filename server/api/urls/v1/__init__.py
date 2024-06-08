from django.urls import path, include

urlpatterns = [
    path("", include("api.urls.v1.general")),
    path("", include("api.urls.v1.shippy")),
    path("", include("api.urls.v1.statistics")),
    path("", include("api.urls.v1.updater")),
]
