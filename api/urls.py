from django.urls import path

from .views import *

urlpatterns = [
    path('v1/updater/', v1_updater, name='v1_updater'),
]