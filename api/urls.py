from django.urls import path

from .views import *

# noinspection SpellCheckingInspection
# remove this once to-do is gone
urlpatterns = [
    path('v1/system/', system_information, name='v1_system_information'),
    path('v1/download/build/counter/', v1_download_build_counter, name='v1_download_build_counter'),
    path('v1/maintainers/login/', maintainer_api_login, name='v1_maintainer_login'),
    path('v1/maintainers/token_check/', maintainer_api_token_check, name='v1_maintainer_token_check'),
    path('v1/maintainers/chunked_upload/', ChunkedBuildUpload.as_view(), name='v1_chunked_build_upload'),
    path('v1/maintainers/chunked_upload/<uuid:pk>/', ChunkedBuildUpload.as_view(), name='chunkedupload-detail'),
    # TODO: rename `chunkedupload-detail` if we can
    path('v1/maintainers/build/enabled_status_modify/', maintainer_api_build_enabled_status_modify,
         name='v1_maintainer_build_enabled_status_modify'),
    path('v1/updater/los/<slug:codename>/<slug:variant>/', v1_updater_los, name='v1_updater_los'),
    path('v2/updater/<slug:codename>/<slug:variant>/', v2_updater_device, name='v2_updater_device'),
    path('v2/all/', v2_all_builds, name='v2_all'),
]
