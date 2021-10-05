from django.urls import path

from .views import *

urlpatterns = [
    # Maintainers
    path('maintainers/', MaintainerDashboardView.as_view(), name='maintainer_dashboard'),
    path('maintainers/device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('maintainers/build/<int:pk>/enabled_status_modify/', build_enabled_status_modify,
         name='build_enabled_status_modify'),
    path('maintainers/build/<int:pk>/delete/', BuildDeleteView.as_view(), name='build_delete'),

    # Admins
    path('admins/statistics/', AdminStatisticsView.as_view(), name='admin_statistics'),
]
