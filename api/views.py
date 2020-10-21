import json

from django.http import HttpResponse, Http404

from django.shortcuts import render, get_object_or_404
from shipper.models import *

# TODO: Implement v2