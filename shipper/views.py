from django.shortcuts import render
from django.views.generic import ListView

from .models import *


class DashboardView(ListView):
    template_name = 'shipper/dashboard.html'
    model = Device