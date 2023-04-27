from django.urls import path

from admin.views import AdminStatisticsView, AdminBuildMirrorStatusView

urlpatterns = [
    path("statistics/", AdminStatisticsView.as_view(), name="admin_statistics"),
    path("mirror_status/", AdminBuildMirrorStatusView.as_view(), name="admin_build_mirror_status"),
]
