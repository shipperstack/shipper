from django.urls import path
from .views import *

urlpatterns = [
    path('maintainers/', MaintainerDashboardView.as_view(), name='dashboard'),
    path('maintainers/device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('maintainers/device/<int:pkd>/build/<int:pk>/', BuildDetailView.as_view(), name='build_detail'),
    path('maintainers/device/<int:pkd>/build/<int:pk>/delete/', BuildDeleteView.as_view(), name='build_delete'),
    path('maintainers/device/<int:pk>/upload/', build_upload, name='build_upload'),
]