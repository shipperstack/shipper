from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory

from downloads.templatetags.build_extras import format_download_url
from downloads.views import DownloadsBuildView, DownloadsDeviceView, DownloadsMainView
from shipper.tests import mock_devices_setup, mock_builds_setup


class ShipperTemplateTagsTestCase(TestCase):
    def test_format_download_url(self):
        self.assertEqual("https://mock/test/Bliss-v14.zip/download/",
                         format_download_url("https://mock/test/{}/download/", "Bliss-v14.zip"))


class DownloadsViewTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        self.factory = RequestFactory()

    def test_downloads_view(self):
        request = self.factory.get("")
        request.user = AnonymousUser()
        response = DownloadsMainView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_downloads_device_bullhead_view(self):
        request = self.factory.get("download/bullhead/")
        request.user = AnonymousUser()
        response = DownloadsDeviceView.as_view()(request, codename="bullhead")

        self.assertEqual(response.status_code, 200)

    def test_downloads_device_invalid_view(self):
        request = self.factory.get("download/invalid/")
        request.user = AnonymousUser()

        with self.assertRaises(Http404):
            DownloadsDeviceView.as_view()(request, codename="invalid")

    def test_downloads_build_bullhead_view(self):
        request = self.factory.get("download/bullhead/1/")
        request.user = AnonymousUser()
        response = DownloadsBuildView.as_view()(request, codename="bullhead", pk=1)

        self.assertEqual(response.status_code, 200)

    def test_downloads_invalid_build_bullhead_view(self):
        request = self.factory.get("download/bullhead/20/")
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            DownloadsBuildView.as_view()(request, codename="bullhead", pk=20)
