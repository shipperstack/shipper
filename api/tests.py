import datetime

from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory

from api.views import parse_build_date, v1_updater_los, v2_updater_device, variant_check, v2_all_builds
from shipper.tests import mock_devices_setup, mock_builds_setup


class APIGeneralTestCase(TestCase):
    def test_parse_build_date(self):
        self.assertEqual(parse_build_date("20200824"), datetime.date(2020, 8, 24))
        self.assertEqual(parse_build_date("20200824").strftime("%s"), "1598227200")

    def test_variant_check(self):
        with self.assertRaises(Http404):
            variant_check("unknown")
        variant_check("gapps")
        variant_check("vanilla")
        variant_check("foss")
        variant_check("goapps")


class APIV1TestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        self.factory = RequestFactory()

    def test_v1_updater_los_bullhead_gapps(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser()
        response = v1_updater_los(request, "bullhead", "gapps")
        expected_response = b'{"response": [{"datetime": 1591574400, "filename": ' \
                            b'"Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip", ' \
                            b'"id": "b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2", ' \
                            b'"size": 857483855, "version": "v14", "variant": "gapps", ' \
                            b'"url": "https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608' \
                            b'.zip", "md5url": ' \
                            b'"https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5' \
                            b'"}]}'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response)

    def test_v1_updater_los_bullhead_vanilla(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        with self.assertRaises(Http404):
            v1_updater_los(request, "bullhead", "vanilla")

    def test_v1_updater_los_bullhead_foss(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        with self.assertRaises(Http404):
            v1_updater_los(request, "bullhead", "foss")

    def test_v1_updater_los_bullhead_goapps(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        with self.assertRaises(Http404):
            v1_updater_los(request, "bullhead", "goapps")


class APIV2TestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        self.factory = RequestFactory()

    def test_v2_updater_bullhead_gapps(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        response = v2_updater_device(request, "bullhead", "gapps")
        expected_response = b'{"date": 1591574400, "file_name": "Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip", ' \
                            b'"sha256": "b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2", ' \
                            b'"size": 857483855, "version": "v14", "zip_download_url": ' \
                            b'"https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip", ' \
                            b'"md5_download_url": ' \
                            b'"https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5"}'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response)

    def test_v2_updater_bullhead_vanilla(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            v2_updater_device(request, "bullhead", "vanilla")

    def test_v2_updater_bullhead_foss(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            v2_updater_device(request, "bullhead", "foss")

    def test_v2_updater_bullhead_goapps(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            v2_updater_device(request, "bullhead", "goapps")

    def test_v2_all_builds(self):
        request = self.factory.get("/api/v2/all/")
        request.user = AnonymousUser()
        response = v2_all_builds(request)
        expected_response = b'{"bullhead": [{"date": 1591574400, "file_name": "Bliss-v14-bullhead-OFFICIAL-gapps-2020' \
                            b'0608.zip", "sha256": "b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2"' \
                            b', "size": 857483855, "version": "v14", "mirrors": [{"name": "Main", "description": "Dow' \
                            b'nload builds from the main server.", "zip_download_url": "https://testserver/media/bull' \
                            b'head/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip", "md5_download_url": "https://test' \
                            b'server/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5"}]}], "angler"' \
                            b': [{"date": 1591574400, "file_name": "Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip", ' \
                            b'"sha256": "b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2", "size": 8' \
                            b'57483855, "version": "v14", "mirrors": [{"name": "Main", "description": "Download build' \
                            b's from the main server.", "zip_download_url": "https://testserver/media/angler/Bliss-v1' \
                            b'4-angler-OFFICIAL-vanilla-20200608.zip", "md5_download_url": "https://testserver/media/' \
                            b'angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip.md5"}]}], "dream2lte": [{"date": ' \
                            b'1591660800, "file_name": "Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip", "sha256": "' \
                            b'b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2", "size": 857483995, "' \
                            b'version": "v14", "mirrors": [{"name": "Main", "description": "Download builds from the ' \
                            b'main server.", "zip_download_url": "https://testserver/media/dream2lte/Bliss-v14-dream2' \
                            b'lte-OFFICIAL-gapps-20200609.zip", "md5_download_url": "https://testserver/media/dream2l' \
                            b'te/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip.md5"}]}]}' \

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response)
