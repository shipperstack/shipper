from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail')
]