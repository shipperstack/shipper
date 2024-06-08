from django.urls import path, include

urlpatterns = [
    path("", include("api.urls.v2.shippy")),
    path("", include("api.urls.v2.statistics")),
]
