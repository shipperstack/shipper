from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory

from shipper.exceptions import UploadException
from shipper.handler import file_name_validity_check
from shipper.models import Device, Build
from shipper.templatetags.build_extras import format_download_url
from shipper.views import DownloadsView, DownloadsDeviceView, DownloadsBuildView, get_codename_from_filename, \
    exception_to_message


class DeviceTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()

    def test_device_string(self):
        devices = get_mock_devices()
        self.assertEqual(str(devices["bullhead"]), "LG Nexus 5X (bullhead)")
        self.assertEqual(str(devices["angler"]), "Huawei Nexus 6P (angler)")
        self.assertEqual(str(devices["dream2lte"]), "Samsung Galaxy S8+ (dream2lte)")

    def test_image_url(self):
        devices = get_mock_devices()
        self.assertEqual(devices["bullhead"].get_photo_url(), "https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg")
        self.assertEqual(devices["angler"].get_photo_url(), "https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg")
        self.assertEqual(devices["dream2lte"].get_photo_url(), "#")


class BuildTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_build_string(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(str(build), "Bliss-v14-bullhead-OFFICIAL-gapps-20200608")

    def test_upload_path(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(build.get_upload_path("example"), "bullhead/example")
        self.assertEqual(build.get_upload_path(""), "bullhead/")

    def test_user_friendly_name(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(build.get_user_friendly_name(), "v14 - June 8, 2020")

    def test_human_readable_size(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(build.get_human_readable_size(), "857.5 MB")

    def test_mirrors(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(len(build.get_enabled_downloadable_mirrors()),  0)


class CombinedTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_gapps_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_gapps_build_objects()), 1)
        self.assertEqual(len(devices["angler"].get_all_gapps_build_objects()), 0)
        self.assertEqual(len(devices["dream2lte"].get_all_gapps_build_objects()), 1)

    def test_vanilla_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_vanilla_build_objects()), 0)
        self.assertEqual(len(devices["angler"].get_all_vanilla_build_objects()), 1)
        self.assertEqual(len(devices["dream2lte"].get_all_vanilla_build_objects()), 0)

    def test_foss_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_foss_build_objects()), 0)
        self.assertEqual(len(devices["angler"].get_all_foss_build_objects()), 0)
        self.assertEqual(len(devices["dream2lte"].get_all_foss_build_objects()), 0)

    def test_goapps_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_goapps_build_objects()), 0)
        self.assertEqual(len(devices["angler"].get_all_goapps_build_objects()), 0)
        self.assertEqual(len(devices["dream2lte"].get_all_goapps_build_objects()), 0)


class HandlerTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_file_name_validity_check(self):
        devices = get_mock_devices()
        with self.assertRaises(UploadException):
            file_name_validity_check(
                device=devices["bullhead"],
                build_file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200609",
                build_type="official",
                codename="bullhead",
                variant="gapps",
            )
        with self.assertRaises(UploadException):
            file_name_validity_check(
                device=devices["bullhead"],
                build_file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200609",
                build_type="OFFICIAL",
                codename="angler",
                variant="gapps",
            )
        with self.assertRaises(UploadException):
            file_name_validity_check(
                device=devices["bullhead"],
                build_file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
                build_type="OFFICIAL",
                codename="bullhead",
                variant="gapps",
            )
        with self.assertRaises(UploadException):
            file_name_validity_check(
                device=devices["bullhead"],
                build_file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200609",
                build_type="OFFICIAL",
                codename="bullhead",
                variant="unknown",
            )


class ViewTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        self.factory = RequestFactory()

    def test_downloads_view(self):
        request = self.factory.get("")
        request.user = AnonymousUser()
        response = DownloadsView.as_view()(request)

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


class HelperFunctionTestCase(TestCase):
    def test_get_codename_from_filename(self):
        self.assertEqual("bullhead", get_codename_from_filename("Bliss-v14.4-bullhead-OFFICIAL-gapps-20200408.zip"))
        self.assertEqual("angler", get_codename_from_filename("Bliss-v14.4-angler-OFFICIAL-vanilla-20200508.zip"))
        self.assertIsNone(get_codename_from_filename("BlissInvalidFileNameWithoutDashes"))
        self.assertIsNone(get_codename_from_filename("Invalid-File-Name.zip.md5"))

    def test_exception_to_message(self):
        self.assertEqual("The file name does not match the checksum file name!",
                         exception_to_message(Exception('file_name_mismatch')))
        self.assertEqual("The file name was malformed. Please do not edit the file name!",
                         exception_to_message(Exception('invalid_file_name')))
        self.assertEqual("Only official builds are allowed.",
                         exception_to_message(Exception('not_official')))
        self.assertEqual("The codename does not match the file!",
                         exception_to_message(Exception('codename_mismatch')))
        self.assertEqual("The build already exists in the system!",
                         exception_to_message(Exception('duplicate_build')))
        self.assertEqual("An unknown error occurred.",
                         exception_to_message(Exception('some_weird_random_error')))
        self.assertEqual("An unknown error occurred.",
                         exception_to_message(Exception('unknown_error')))


class TemplateTagsTestCase(TestCase):
    def test_format_download_url(self):
        self.assertEqual("https://mock/test/Bliss-v14.zip/download/",
                         format_download_url("https://mock/test/{}/download/", "Bliss-v14.zip"))


def mock_devices_setup():
    Device.objects.create(
        name="Nexus 5X",
        codename="bullhead",
        manufacturer="LG",
        photo="https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg",
        status=True,
    )
    Device.objects.create(
        name="Nexus 6P",
        codename="angler",
        manufacturer="Huawei",
        photo="https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg",
        status=False,
    )
    Device.objects.create(
        name="Galaxy S8+",
        codename="dream2lte",
        manufacturer="Samsung",
        status=True,
    )
    Device.objects.create(
        name="No Builds",
        codename="nobuild",
        manufacturer="NoBuilds",
        status=False,
    )


def get_mock_devices():
    devices = {
        "bullhead": Device.objects.get(codename="bullhead"),
        "angler": Device.objects.get(codename="angler"),
        "dream2lte": Device.objects.get(codename="dream2lte"),
    }
    return devices


def mock_builds_setup():
    Build.objects.create(
        device=Device.objects.get(codename="bullhead"),
        file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
        zip_file="bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
        md5_file="bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5",
    )
    Build.objects.create(
        device=Device.objects.get(codename="dream2lte"),
        file_name="Bliss-v14-dream2lte-OFFICIAL-gapps-20200609",
        size=857483995,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
        zip_file="dream2lte/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip",
        md5_file="dream2lte/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip.md5",
    )
    Build.objects.create(
        device=Device.objects.get(codename="angler"),
        file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="vanilla",
        zip_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip",
        md5_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip.md5",
    )
