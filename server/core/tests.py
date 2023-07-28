from django.test import TestCase, override_settings

from .exceptions import UploadException
from .models import Build, Device
from .utils import is_version_in_target_versions, parse_filename_with_regex


device_build_pairing = {}


class ShipperDeviceTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()

    def test_device_string(self):
        for device in Device.objects.all():
            self.assertEqual(
                str(device), f"{device.manufacturer} {device.name} ({device.codename})"
            )


class ShipperBuildTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_build_string(self):
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        self.assertEqual(str(build), "Bliss-v14-bullhead-OFFICIAL-gapps-20200608")

    def test_upload_path(self):
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        self.assertEqual(build.get_upload_path("example"), "bullhead/example")
        self.assertEqual(build.get_upload_path(""), "bullhead/")

    def test_user_friendly_name(self):
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        self.assertEqual(build.get_user_friendly_name(), "v14 - 2020-06-08")

    def test_human_readable_size(self):
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        self.assertEqual(build.get_human_readable_size(), "857.5 MB")

    def test_mirrors(self):
        build = Build.objects.get(
            file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"
        )
        self.assertEqual(len(build.get_downloadable_mirrors()), 0)


class ShipperCombinedTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()

    def test_gapps_build_count(self):
        self.test_variant_build_count(variant="gapps")

    def test_vanilla_build_count(self):
        self.test_variant_build_count(variant="vanilla")

    def test_foss_build_count(self):
        self.test_variant_build_count(variant="foss")

    def test_goapps_build_count(self):
        self.test_variant_build_count(variant="goapps")

    def test_variant_build_count(self, variant=None):
        if not variant:
            return

        for device in Device.objects.all():
            if (
                device.codename in device_build_pairing
                and variant in device_build_pairing[device.codename]
            ):
                build_count = device_build_pairing[device.codename][variant]
            else:
                build_count = 0
            self.assertEqual(
                len(device.get_all_enabled_hashed_builds_of_variant(variant=variant)),
                build_count,
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

    @override_settings(
        SHIPPER_FILE_NAME_FORMAT="[A-Za-z]*-(?P<version>[a-z0-9.]*)-(?P<codename>[A-Za-"
        "z]*)-OFFICIAL-(?P<variant>[a-z]*)-(?P<date>[0-9]*).zip"
    )
    def test_parse_filename_with_regex_invalid_filename(self):
        with self.assertRaises(UploadException):
            parse_filename_with_regex("whatever.zip")
        with self.assertRaises(UploadException):
            parse_filename_with_regex(
                "Bliss-v12.8-bullhead-OFFICIAL-gapps-20210820.mp4"
            )
        with self.assertRaises(UploadException):
            parse_filename_with_regex(
                "Bliss-bullhead-v12.8-OFFICIAL-gapps-20210820.zip"
            )

    @override_settings(
        SHIPPER_FILE_NAME_FORMAT="[A-Za-z]*-(?P<version>[a-z0-9.]*)-(?P<codename>[A-Za-"
        "z]*)-OFFICIAL-(?P<variant>[a-z]*)-(?P<date>[0-9]*).zip"
    )
    def test_parse_filename_with_regex(self):
        self.assertEqual(
            parse_filename_with_regex(
                "Bliss-v12.8-bullhead-OFFICIAL-gapps-20210820.zip"
            )["version"],
            "v12.8",
        )
        self.assertEqual(
            parse_filename_with_regex(
                "Bliss-v12.8-bullhead-OFFICIAL-gapps-20210820.zip"
            )["codename"],
            "bullhead",
        )
        self.assertEqual(
            parse_filename_with_regex(
                "Bliss-v12.8-bullhead-OFFICIAL-gapps-20210820.zip"
            )["variant"],
            "gapps",
        )
        self.assertEqual(
            parse_filename_with_regex(
                "Bliss-v12.8-bullhead-OFFICIAL-gapps-20210820.zip"
            )["date"],
            "20210820",
        )


def mock_devices_setup():
    Device.objects.create(
        name="Nexus 5X",
        codename="bullhead",
        manufacturer="LG",
        photo="https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg",
        status=True,
    )
    device_build_pairing["bullhead"] = {}

    Device.objects.create(
        name="Nexus 6P",
        codename="angler",
        manufacturer="Huawei",
        photo="https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg",
        status=False,
    )
    device_build_pairing["angler"] = {}

    Device.objects.create(
        name="Galaxy S8+",
        codename="dream2lte",
        manufacturer="Samsung",
        status=True,
    )
    device_build_pairing["dream2lte"] = {}

    Device.objects.create(name="x86", codename="x86", manufacturer="x86", status=True)
    device_build_pairing["x86"] = {}

    # noinspection SpellCheckingInspection
    Device.objects.create(
        name="No Builds",
        codename="nobuild",
        manufacturer="NoBuilds",
        status=False,
    )
    device_build_pairing["nobuild"] = {}


def mock_builds_setup():
    from datetime import date

    Build.objects.create(
        device=Device.objects.get(codename="bullhead"),
        file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
        size=857483855,
        version="v14",
        md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
        build_date=date(2020, 6, 8),
        zip_file="bullhead/Bliss-v14-bullhead-OFFICIAL-gapps-20200608.zip",
    )
    device_build_pairing["bullhead"]["gapps"] = 1

    Build.objects.create(
        device=Device.objects.get(codename="dream2lte"),
        file_name="Bliss-v14-dream2lte-OFFICIAL-gapps-20200609",
        size=857483995,
        version="v14",
        md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
        build_date=date(2020, 6, 9),
        zip_file="dream2lte/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip",
    )
    device_build_pairing["dream2lte"]["gapps"] = 1

    Build.objects.create(
        device=Device.objects.get(codename="angler"),
        file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
        variant="vanilla",
        build_date=date(2020, 6, 8),
        zip_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip",
    )
    device_build_pairing["angler"]["vanilla"] = 1
