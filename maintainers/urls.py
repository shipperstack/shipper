from django.urls import path

from .views import (
    BuildDeleteView,
    DeviceDetailView,
    MaintainerDashboardView,
    build_enabled_status_modify,
)

urlpatterns = [
    path(
        "", MaintainerDashboardView.as_view(), name="maintainer_dashboard"
    ),
    path(
        "device/<int:pk>/", DeviceDetailView.as_view(), name="device_detail"
    ),
    path(
        "build/<int:pk>/enabled_status_modify/",
        build_enabled_status_modify,
        name="build_enabled_status_modify",
    ),
    path(
        "build/<int:pk>/delete/",
        BuildDeleteView.as_view(),
        name="build_delete",
    ),
]
