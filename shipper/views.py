from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'shipper/dashboard.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/device_detail.html'
    model = Device


class BuildDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/build_detail.html'
    model = Build

