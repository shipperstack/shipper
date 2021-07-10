from django.urls import path

from .views import *

# noinspection SpellCheckingInspection
# remove this once to-do is gone
urlpatterns = [
    path('v1/system/info/', v1_system_info, name='v1_system_info'),
    path('v1/download/build/counter/', v1_download_build_counter, name='v1_download_build_counter'),
    path('v1/maintainers/login/', v1_maintainers_login, name='v1_maintainers_login'),
    path('v1/maintainers/token_check/', v1_maintainers_token_check, name='v1_maintainers_token_check'),
    path('v1/maintainers/chunked_upload/', V1MaintainersChunkedUpload.as_view(), name='v1_maintainers_chunked_upload'),
    path('v1/maintainers/chunked_upload/<uuid:pk>/', V1MaintainersChunkedUpload.as_view(), name='chunkedupload-detail'),
    # TODO: rename `chunkedupload-detail` if we can
    path('v1/maintainers/build/enabled_status_modify/', v1_maintainers_build_enabled_status_modify,
         name='v1_maintainers_build_enabled_status_modify'),
    path('v1/updater/los/<slug:codename>/<slug:variant>/', v1_updater_los, name='v1_updater_los'),
    path('v2/updater/<slug:codename>/<slug:variant>/', v2_updater_device, name='v2_updater_device'),
    path('v2/all/', v2_all_builds, name='v2_all'),
]
