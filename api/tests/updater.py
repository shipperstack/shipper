from api.utils import variant_check
from api.views import V1UpdaterLOS
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory, APITestCase
from shipper.tests import mock_builds_setup, mock_devices_setup


class UpdaterTestCase(APITestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        self.factory = APIRequestFactory()
        V1UpdaterLOS.throttle_classes = ()

    def test_variant_check(self):
        response = variant_check("unknown")
        self.assertEqual(response.status_code, 400)

        self.assertIsNone(variant_check("gapps"))
        self.assertIsNone(variant_check("vanilla"))
        self.assertIsNone(variant_check("foss"))
        self.assertIsNone(variant_check("goapps"))

    def test_v1_updater_los_bullhead_gapps(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser()
        response = V1UpdaterLOS.as_view()(request, "bullhead", "gapps")

        self.assertEqual(response.status_code, 200)

        self.assertIn("response", response.data)
        self.assertIn("datetime", response.data["response"][0])
        self.assertIn("filename", response.data["response"][0])
        self.assertIn("id", response.data["response"][0])
        self.assertIn("size", response.data["response"][0])
        self.assertIn("version", response.data["response"][0])
        self.assertIn("variant", response.data["response"][0])
        self.assertIn("url", response.data["response"][0])
        self.assertIn("md5url", response.data["response"][0])

        self.assertEqual(1591574400, response.data["response"][0]["datetime"])
        self.assertEqual(
            "Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
            response.data["response"][0]["filename"],
        )
        self.assertEqual(
            "b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
            response.data["response"][0]["id"],
        )
        self.assertEqual(857483855, response.data["response"][0]["size"])
        self.assertEqual("v14", response.data["response"][0]["version"])
        self.assertEqual("gapps", response.data["response"][0]["variant"])
        self.assertEqual(
            "https://testserver/media/bullhead/"
            "Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
            response.data["response"][0]["url"],
        )
        self.assertEqual(
            "https://testserver/media/bullhead/"
            "Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5",
            response.data["response"][0]["md5url"],
        )

    def test_v1_updater_los_bullhead_vanilla(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = V1UpdaterLOS.as_view()(request, "bullhead", "vanilla")

        self.assertEqual(response.status_code, 404)

    def test_v1_updater_los_bullhead_foss(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = V1UpdaterLOS.as_view()(request, "bullhead", "foss")

        self.assertEqual(response.status_code, 404)

    def test_v1_updater_los_bullhead_goapps(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = V1UpdaterLOS.as_view()(request, "bullhead", "goapps")

        self.assertEqual(response.status_code, 404)

    def test_v1_updater_los_nonexistent_device(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = V1UpdaterLOS.as_view()(request, "nonexistent", "gapps")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["message"], "The specified device does not exist!"
        )

    def test_v1_updater_los_nonexistent_variant(self):
        request = self.factory.get("/api/v1/updater/los/")
        request.user = AnonymousUser
        response = V1UpdaterLOS.as_view()(request, "bullhead", "milkshake")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["message"],
            "Wrong parameter. Try with the correct parameters.",
        )
