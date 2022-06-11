from django.urls import path

from .views import AdminStatisticsView

urlpatterns = [
    path("admins/statistics/", AdminStatisticsView.as_view(), name="admin_statistics"),
]
