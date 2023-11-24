from api.views import v1_maintainers_login, v1_system_info
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from core.models import Build, Device
from core.tests.base import mock_setup

User = get_user_model()


class ShippyTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.credentials = {
            "username": "maintainer_user_1",
            "password": "password",
        }
        self.user = User.objects.create_user(**self.credentials)
        self.token = Token.objects.get_or_create(user=self.user)

        # Set up mock targets
        mock_setup()

        # Add dummy user to mock device bullhead
        Device.objects.get(codename="bullhead").maintainers.add(self.user)

    def test_v1_system_info(self):
        request = self.factory.get("/api/v1/system/info/")
        request.user = AnonymousUser()
        response = v1_system_info(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["version"], settings.SHIPPER_VERSION)

    def test_v1_maintainers_login(self):
        request = self.factory.post("/api/v1/maintainers/login/", data=self.credentials)
        response = v1_maintainers_login(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_v1_maintainers_login_invalid(self):
        incorrect_credentials = {
            "username": "maintainer_user_1",
            "password": "incorrect",
        }
        request = self.factory.post(
            "/api/v1/maintainers/login/", data=incorrect_credentials
        )
        response = v1_maintainers_login(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "invalid_credential")

    def test_v1_maintainers_login_missing_password_field(self):
        missing_credentials = {"username": "user1"}
        request = self.factory.post(
            "/api/v1/maintainers/login/", data=missing_credentials
        )
        response = v1_maintainers_login(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "blank_username_or_password")

    def test_v1_maintainers_login_missing_username_field(self):
        missing_credentials = {"password": "hunter2"}
        request = self.factory.post(
            "/api/v1/maintainers/login/", data=missing_credentials
        )
        response = v1_maintainers_login(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "blank_username_or_password")

    def test_v1_maintainers_token_check(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token[0]))
        response = self.client.get("/api/v1/maintainers/token_check/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.credentials["username"])

    def test_v1_maintainers_build_enabled_status_modify_disable(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token[0]))
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        data = {"build_id": build.id, "enable": False}
        response = self.client.post(
            "/api/v1/maintainers/build/enabled_status_modify/", data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successfully disabled the build!")

    def test_v1_maintainers_build_enabled_status_modify_enable(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token[0]))
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        data = {"build_id": build.id, "enable": True}
        response = self.client.post(
            "/api/v1/maintainers/build/enabled_status_modify/", data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successfully enabled the build!")

    def test_v1_maintainers_build_enabled_status_modify_missing_build_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token[0]))
        data = {"enable": False}
        response = self.client.post(
            "/api/v1/maintainers/build/enabled_status_modify/", data=data
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "missing_parameters")

    def test_v1_maintainers_build_enabled_status_modify_missing_enable(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token[0]))
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        data = {"build_id": build.id}
        response = self.client.post(
            "/api/v1/maintainers/build/enabled_status_modify/", data=data
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "missing_parameters")

    def test_v1_maintainer_build_enabled_status_modify_insufficient_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token[0]))
        build = Build.objects.get(
            file_name="Bliss-v14-dream2lte-OFFICIAL-gapps-20200609"
        )
        data = {"build_id": build.id, "enable": False}
        response = self.client.post(
            "/api/v1/maintainers/build/enabled_status_modify/", data=data
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["error"], "insufficient_permissions")
