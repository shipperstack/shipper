from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView
from drf_chunked_upload.views import ChunkedUploadView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_401_UNAUTHORIZED

from config.settings import SHIPPER_VERSION
from .forms import *
from .handler import *
from .models import *


class DownloadsView(ListView):
    template_name = 'shipper/downloads.html'
    model = Device

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'main_website_url': settings.MAIN_WEBSITE_URL,
            'downloads_page_main_branding': settings.DOWNLOADS_PAGE_MAIN_BRANDING
        }
        return super().get(request, *args, **kwargs)


class DownloadsDeviceView(DetailView):
    template_name = 'shipper/downloads_device.html'
    model = Device

    def get_object(self, queryset=None):
        return Device.objects.get(codename=self.kwargs.get("codename"))

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'main_website_url': settings.MAIN_WEBSITE_URL,
            'downloads_page_main_branding': settings.DOWNLOADS_PAGE_MAIN_BRANDING,
            'downloads_page_donation_url': settings.DOWNLOADS_PAGE_DONATION_URL
        }
        return super().get(request, *args, **kwargs)


class MaintainerDashboardView(LoginRequiredMixin, ListView):
    template_name = 'shipper/maintainer_dashboard.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shipper/device_detail.html'
    model = Device

    # Override devices shown to maintainers
    def get_queryset(self):
        return Device.objects.filter(maintainers=self.request.user)


class BuildDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'shipper/build_delete.html'
    model = Build

    def get_success_url(self):
        return reverse('device_detail', kwargs={'pk': self.get_object().device.id})

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.get_object().delete()
        return HttpResponseRedirect(success_url)

    # Override builds shown to maintainers
    def get_queryset(self):
        return Build.objects.filter(device__maintainers=self.request.user)


@login_required
def build_upload(request, pk):
    device = get_object_or_404(Device, pk=pk)

    # Check if maintainer is in device's approved maintainers list
    if request.user not in device.maintainers.all():
        raise Http404

    if request.method == 'POST':
        form = BuildUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_build(device, request.FILES["zip_file"], request.FILES["md5_file"])
            except UploadException as exception:
                return render(request, 'shipper/build_upload.html', {
                    'upload_succeeded': False,
                    'error_reason': str(exception),
                    'device': device,
                    'form': form
                })

            return render(request, 'shipper/build_upload.html', {
                'upload_succeeded': True,
                'device': device,
                'form': form
            })
        return render(request, 'shipper/build_upload.html', {
            'upload_succeeded': False,
            'error_reason': 'invalid_form',
            'device': device,
            'form': form
        })

    form = BuildUploadForm()
    return render(request, 'shipper/build_upload.html', {
        'form': form,
        'device': device
    })


class ChunkedBuildUpload(ChunkedUploadView):
    def on_completion(self, uploaded_file, request):
        device_codename = get_codename_from_filename(uploaded_file.filename)
        device = get_object_or_404(Device, codename=device_codename)

        # Check if maintainer is in device's approved maintainers list
        if self.request.user not in device.maintainers.all():
            raise Http404

        try:
            handle_chunked_build(device, uploaded_file.filename, uploaded_file, request.POST.get('md5'))
        except UploadException as exception:
            return Response(
                {
                    'error': str(exception),
                    'message': exception_to_message(exception)
                },
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'message': 'Build has been uploaded for device {}!'.format(device)
            },
            status=HTTP_200_OK
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def maintainer_api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {
                'error': 'blank_username_or_password',
                'message': 'Username or password cannot be blank!'
            },
            status=HTTP_400_BAD_REQUEST
        )
    user = authenticate(username=username, password=password)
    if not user:
        return Response({
            'error': 'invalid_credential',
            'message': 'Invalid credentials. Please try again.'
        },
            status=HTTP_404_NOT_FOUND
        )
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key,
            'message': 'Successfully logged in!'
        },
        status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
def maintainer_api_build_upload(request):
    device = Device.objects.get(codename=get_codename_from_filename(request.FILES["zip_file"].name))

    # Check if device exists
    if device is None:
        raise Http404

    build_file = request.data.get("build_file")
    checksum_file = request.data.get("checksum_file")

    # If any of the fields are blank, fail immediately
    if build_file is None or checksum_file is None:
        return Response(
            {
                'error': 'missing_files',
                'message': 'One or more required files are missing.'
            },
            status=HTTP_400_BAD_REQUEST
        )

    # Check if user has sufficient permission to upload builds for given codename
    if device not in Device.objects.filter(maintainers=request.user):
        return Response(
            {
                'error': 'insufficient_permissions',
                'message': 'You are not authorized to upload for this device!'
            },
            status=HTTP_401_UNAUTHORIZED
        )

    try:
        handle_build(device, build_file, checksum_file)
    except UploadException as exception:
        return Response(
            {
                'error': str(exception),
                'message': exception_to_message(exception)
            },
            status=HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            'message': 'Build has been uploaded for device {}!'.format(device)
        },
        status=HTTP_200_OK
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def system_information(request):
    return Response(
        {
            'version': SHIPPER_VERSION
        }
    )


def get_codename_from_filename(filename):
    try:
        _, version, codename, build_type, variant, date = os.path.splitext(filename)[0].split('-')
        return codename
    except ValueError:
        return None


def exception_to_message(e):
    e = str(e)
    if e == 'file_name_mismatch':
        return "The file name does not match the checksum file name!"
    if e == 'invalid_file_name':
        return "The file name was malformed. Please do not edit the file name!"
    if e == 'not_official':
        return "Only official builds are allowed."
    if e == 'codename_mismatch':
        return "The codename does not match the file!"
    if e == 'duplicate_build':
        return "The build already exists in the system!"
    return "An unknown error occurred."
