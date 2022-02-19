from django.test import TestCase, override_settings


from .exceptions import *
from .handler import file_name_validity_check
from .models import Device, Build
from .utils import *


class ShipperDeviceTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()

    def test_device_string(self):
        devices = get_mock_devices()
        self.assertEqual(str(devices["bullhead"]), "LG Nexus 5X (bullhead)")
        self.assertEqual(str(devices["angler"]), "Huawei Nexus 6P (angler)")
        self.assertEqual(str(devices["dream2lte"]), "Samsung Galaxy S8+ (dream2lte)")


class ShipperBuildTestCase(TestCase):
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
        self.assertEqual(build.get_user_friendly_name(), "v14 - 2020-06-08")

    def test_human_readable_size(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(build.get_human_readable_size(), "857.5 MB")

    def test_mirrors(self):
        build = Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608")
        self.assertEqual(len(build.get_downloadable_mirrors()), 0)


class ShipperCombinedTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_gapps_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_enabled_hashed_builds_of_variant(variant="gapps")), 1)
        self.assertEqual(len(devices["angler"].get_all_enabled_hashed_builds_of_variant(variant="gapps")), 0)
        self.assertEqual(len(devices["dream2lte"].get_all_enabled_hashed_builds_of_variant(variant="gapps")), 1)

    def test_vanilla_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_enabled_hashed_builds_of_variant(variant="vanilla")), 0)
        self.assertEqual(len(devices["angler"].get_all_enabled_hashed_builds_of_variant(variant="vanilla")), 1)
        self.assertEqual(len(devices["dream2lte"].get_all_enabled_hashed_builds_of_variant(variant="vanilla")), 0)

    def test_foss_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_enabled_hashed_builds_of_variant(variant="foss")), 0)
        self.assertEqual(len(devices["angler"].get_all_enabled_hashed_builds_of_variant(variant="foss")), 0)
        self.assertEqual(len(devices["dream2lte"].get_all_enabled_hashed_builds_of_variant(variant="foss")), 0)

    def test_goapps_build_count(self):
        devices = get_mock_devices()
        self.assertEqual(len(devices["bullhead"].get_all_enabled_hashed_builds_of_variant(variant="goapps")), 0)
        self.assertEqual(len(devices["angler"].get_all_enabled_hashed_builds_of_variant(variant="goapps")), 0)
        self.assertEqual(len(devices["dream2lte"].get_all_enabled_hashed_builds_of_variant(variant="goapps")), 0)


class ShipperHandlerTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_file_name_validity_check(self):
        with self.assertRaises(UploadException):
            file_name_validity_check(
                build_file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200609",
                variant="unknown",
            )


class ShipperUtilsTestCase(TestCase):
    def test_is_version_in_target_versions_empty_target_versions(self):
        self.assertFalse(is_version_in_target_versions("v12.5", ""))

    def test_is_version_in_target_versions_all_target_versions(self):
        self.assertTrue(is_version_in_target_versions("v12.5", "*"))
        self.assertTrue(is_version_in_target_versions("v10.1", "*"))

    def test_is_version_in_target_versions_wildcard_matching(self):
        self.assertTrue(is_version_in_target_versions("v12.5", "v12.*"))
        self.assertTrue(is_version_in_target_versions("v12.20", "v12.*"))
        self.assertTrue(is_version_in_target_versions("v12.108", "v12.*"))
        self.assertTrue(is_version_in_target_versions("v12.5", "v12.*\nv11.8"))
        self.assertTrue(is_version_in_target_versions("v12.20", "v12.*\nv11.8"))
        self.assertTrue(is_version_in_target_versions("v12.108", "v12.*\nv11.8"))
        self.assertFalse(is_version_in_target_versions("v12.5", "v11.*"))
        self.assertFalse(is_version_in_target_versions("v12.20", "v11.*"))
        self.assertFalse(is_version_in_target_versions("v12.108", "v11.*"))

    def test_is_version_in_target_versions_exact_matching(self):
        self.assertTrue(is_version_in_target_versions("v12.5", "v12.5"))
        self.assertFalse(is_version_in_target_versions("v12.5", "v12.6"))

    def test_is_version_in_target_versions_invalid_wildcard_version(self):
        with self.assertRaises(Exception):
            is_version_in_target_versions("v12.*", "v12.*")

    @override_settings(SHIPPER_FILE_NAME_FORMAT='[A-Za-z]*-(?P<version>[a-z0-9.]*)-(?P<codename>[A-Za-z]*)-OFFICIAL-(?P<variant>[a-z]*)-(?P<date>[0-9]*).zip')
    def test_parse_filename_with_regex_invalid_filename(self):
        with self.assertRaises(RegexParseException):
            parse_filename_with_regex("whatever.zip")
        with self.assertRaises(RegexParseException):
            parse_filename_with_regex("Bliss-v12.8-bullhead-OFFICIAL-gapps-20210820.mp4")
        with self.assertRaises(RegexParseException):
            parse_filename_with_regex("Bliss-bullhead-v12.8-OFFICIAL-gapps-20210820.zip")


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
    # noinspection SpellCheckingInspection
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
    from datetime import date
    Build.objects.create(
        device=Device.objects.get(codename="bullhead"),
        file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
        build_date=date(2020, 6, 8),
        zip_file="bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
        md5_file="bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip.md5",
        download_count=20,
    )
    Build.objects.create(
        device=Device.objects.get(codename="dream2lte"),
        file_name="Bliss-v14-dream2lte-OFFICIAL-gapps-20200609",
        size=857483995,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
        build_date=date(2020, 6, 9),
        zip_file="dream2lte/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip",
        md5_file="dream2lte/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip.md5",
        download_count=40,
    )
    Build.objects.create(
        device=Device.objects.get(codename="angler"),
        file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="vanilla",
        build_date=date(2020, 6, 8),
        zip_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip",
        md5_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip.md5",
        download_count=60,
    )
