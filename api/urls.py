from django.urls import path

from .views import *

urlpatterns = [
    path('v1/download/build/counter/', v1_download_build_counter, name='v1_download_build_counter'),
    path('v1/updater/los/<slug:codename>/<slug:variant>/', v1_updater_los, name='v1_updater_los'),
    path('v2/updater/<slug:codename>/<slug:variant>/', v2_updater_device, name='v2_updater_device'),
    path('v2/all/', v2_all_builds, name='v2_all'),
]
