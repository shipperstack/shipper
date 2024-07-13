from django.urls import path, include

urlpatterns = [
    path("latest/", include("api.urls.latest")),
    path("v1/", include("api.urls.v1")),
    path("v2/", include("api.urls.v2")),
]
