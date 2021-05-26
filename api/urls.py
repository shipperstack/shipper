from django.urls import path

from .views import *

urlpatterns = [
    path('v1/updater/los/<slug:codename>/<slug:variant>/', v1_updater_los, name='v1_updater_los'),
    path('v2/updater/<slug:codename>/<slug:variant>/', v2_updater_device, name='v2_updater_device'),
    path('v1/internal/device/list/', v1_internal_device_list, name='v1_internal_device_list'),
    path('v1/internal/device/add/', v1_internal_device_add, name='v1_internal_device_add'),
    path('v1/internal/maintainer/list/', v1_internal_maintainer_list, name='v1_internal_maintainer_list'),
]
