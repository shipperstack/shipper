import datetime

from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import parse_build_date, v1_updater_los, v2_updater_device, variant_check, get_codename_from_filename, \
    v1_system_info, v1_maintainers_login
from config.settings import SHIPPER_VERSION
from shipper.tests import mock_devices_setup, mock_builds_setup


class UpdaterTestCase(APITestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        self.factory = APIRequestFactory()

    def test_parse_build_date(self):
        self.assertEqual(parse_build_date("20200824"), datetime.date(2020, 8, 24))
        self.assertEqual(parse_build_date("20200824").strftime("%s"), "1598227200")

    def test_variant_check(self):
        response = variant_check("unknown")
        self.assertEqual(response.status_code, 400)

        self.assertIsNone(variant_check("gapps"))
        self.assertIsNone(variant_check("vanilla"))
        self.assertIsNone(variant_check("foss"))
        self.assertIsNone(variant_check("goapps"))

    def test_get_codename_from_filename(self):
        self.assertEqual("bullhead", get_codename_from_filename("Bliss-v14.4-bullhead-OFFICIAL-gapps-20200408.zip"))
        self.assertEqual("angler", get_codename_from_filename("Bliss-v14.4-angler-OFFICIAL-vanilla-20200508.zip"))
        self.assertIsNone(get_codename_from_filename("BlissInvalidFileNameWithoutDashes"))
        self.assertIsNone(get_codename_from_filename(""))
        self.assertIsNone(get_codename_from_filename("Invalid-File-Name.zip.md5"))

    def test_v1_updater_los_bullhead_gapps(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser()
        response = v1_updater_los(request, "bullhead", "gapps")

        self.assertEqual(response.status_code, 200)

        self.assertIn("response", response.data)
        self.assertIn("datetime", response.data['response'][0])
        self.assertIn("filename", response.data['response'][0])
        self.assertIn("id", response.data['response'][0])
        self.assertIn("size", response.data['response'][0])
        self.assertIn("version", response.data['response'][0])
        self.assertIn("variant", response.data['response'][0])
        self.assertIn("url", response.data['response'][0])
        self.assertIn("md5url", response.data['response'][0])

        self.assertEqual(1591574400, response.data['response'][0]['datetime'])
        self.assertEqual("Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip", response.data['response'][0]['filename'])
        self.assertEqual("b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
                         response.data['response'][0]['id'])
        self.assertEqual(857483855, response.data['response'][0]['size'])
        self.assertEqual("v14", response.data['response'][0]['version'])
        self.assertEqual("gapps", response.data['response'][0]['variant'])
        self.assertEqual("https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
                         response.data['response'][0]['url'])
        self.assertEqual("https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5",
                         response.data['response'][0]['md5url'])

    def test_v1_updater_los_bullhead_vanilla(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = v1_updater_los(request, "bullhead", "vanilla")

        self.assertEqual(response.status_code, 404)

    def test_v1_updater_los_bullhead_foss(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = v1_updater_los(request, "bullhead", "foss")

        self.assertEqual(response.status_code, 404)

    def test_v1_updater_los_bullhead_goapps(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = v1_updater_los(request, "bullhead", "goapps")

        self.assertEqual(response.status_code, 404)

    def test_v2_updater_bullhead_gapps(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        response = v2_updater_device(request, "bullhead", "gapps")

        self.assertEqual(response.status_code, 200)

        self.assertIn("date", response.data)
        self.assertIn("file_name", response.data)
        self.assertIn("sha256", response.data)
        self.assertIn("size", response.data)
        self.assertIn("version", response.data)
        self.assertIn("zip_download_url", response.data)
        self.assertIn("md5_download_url", response.data)

        self.assertEqual(1591574400, response.data['date'])
        self.assertEqual("Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip", response.data['file_name'])
        self.assertEqual("b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2", response.data['sha256'])
        self.assertEqual(857483855, response.data['size'])
        self.assertEqual("v14", response.data['version'])
        self.assertEqual("https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
                         response.data['zip_download_url'])
        self.assertEqual("https://testserver/media/bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5",
                         response.data['md5_download_url'])

    def test_v2_updater_bullhead_vanilla(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        response = v2_updater_device(request, "bullhead", "vanilla")

        self.assertEqual(response.status_code, 404)

    def test_v2_updater_bullhead_foss(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        response = v2_updater_device(request, "bullhead", "foss")

        self.assertEqual(response.status_code, 404)

    def test_v2_updater_bullhead_goapps(self):
        request = self.factory.get("/api/v2/updater/")
        request.user = AnonymousUser()
        response = v2_updater_device(request, "bullhead", "goapps")

        self.assertEqual(response.status_code, 404)


class ShippyTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.credentials = {
            'username': 'maintainer_user_1',
            'password': 'password',
        }
        User.objects.create_user(**self.credentials)

    def test_v1_system_info(self):
        request = self.factory.get("api/v1/system/info/")
        request.user = AnonymousUser()
        response = v1_system_info(request).render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['version'], SHIPPER_VERSION)

    def test_v1_maintainers_login_invalid(self):
        incorrect_credentials = {
            'username': 'maintainer_user_1',
            'password': 'incorrect'
        }
        request = self.factory.post("api/v1/maintainers/login/", data=incorrect_credentials)
        response = v1_maintainers_login(request).render()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'invalid_credential')
