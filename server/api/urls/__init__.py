from django.urls import path, include
from rest_framework.schemas import get_schema_view

from config import settings

urlpatterns = [
    # OpenAPI schema
    path(
        "openapi/",
        get_schema_view(
            title="shipper", description="shipper API", version=settings.SHIPPER_VERSION
        ),
        name="openapi-schema",
    ),
    path("latest/", include("api.urls.latest")),
    path("v1/", include("api.urls.v1")),
    path("v2/", include("api.urls.v2")),
]
