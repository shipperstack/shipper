from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from api.views import v1_system_info, v1_maintainers_login, exception_to_message
from shipper.models import Build, Device
from shipper.tests import mock_devices_setup, mock_builds_setup

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
        mock_devices_setup()
        mock_builds_setup()

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

    def test_exception_to_message(self):
        self.assertEqual(
            "The file name does not match the checksum file name!",
            exception_to_message(Exception("file_name_mismatch")),
        )
        self.assertEqual(
            "The file name was malformed. Please do not edit the file name!",
            exception_to_message(Exception("invalid_file_name")),
        )
        self.assertEqual(
            "Only official builds are allowed.",
            exception_to_message(Exception("not_official")),
        )
        self.assertEqual(
            "The codename does not match the file!",
            exception_to_message(Exception("codename_mismatch")),
        )
        self.assertEqual(
            "The build already exists in the system!",
            exception_to_message(Exception("duplicate_build")),
        )
        self.assertEqual(
            "An unknown error occurred.",
            exception_to_message(Exception("some_weird_random_error")),
        )
        self.assertEqual(
            "An unknown error occurred.",
            exception_to_message(Exception("unknown_error")),
        )
