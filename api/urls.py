from django.urls import path

from .views import *

urlpatterns = [
    path('v2/updater/<slug:codename>/<slug:gapps>/', v2_updater_device, name='v2_updater_device'),
]