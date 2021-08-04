from django.urls import path

from .views import *

urlpatterns = [
    path('', DownloadsMainView.as_view(), name='downloads'),
    path('download/<slug:codename>/', DownloadsDeviceView.as_view(), name='downloads_device'),
    path('download/<slug:codename>/<int:pk>/', DownloadsBuildView.as_view(), name='downloads_build'),
]
