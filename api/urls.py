from django.urls import path

from .views import *

urlpatterns = [
    path('v1/updater/', v1_updater, name='v1_updater'),
    path('v1/updater/<slug:codename>/<slug:release>/', v1_updater_device, name='v1_updater_device'),
]