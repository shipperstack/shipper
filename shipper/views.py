from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'shipper/dashboard.html'
    model = Device