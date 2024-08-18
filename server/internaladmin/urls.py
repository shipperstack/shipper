from django.urls import path

from internaladmin.views import (
    AdminStatisticsView,
    AdminBuildMirrorStatusView,
    AdminMainView,
)

urlpatterns = [
    path("", AdminMainView.as_view(), name="admin_main"),
    path("statistics/", AdminStatisticsView.as_view(), name="admin_statistics"),
    path(
        "mirror_status/",
        AdminBuildMirrorStatusView.as_view(),
        name="admin_build_mirror_status",
    ),
]
