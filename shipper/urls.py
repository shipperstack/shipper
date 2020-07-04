from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('device/<int:pk>/build/<int:pkb>/', BuildDetailView.as_view(), name='build_detail'),
    path('device/<int:pk>/build/<int:pkb>/delete', BuildDeleteView.as_view(), name='build_delete'),
    path('device/<int:pk>/upload/', build_upload, name='build_upload'),
]