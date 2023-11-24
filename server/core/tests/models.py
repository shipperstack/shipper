from django.test import TestCase

from core.models import Build, Device
from core.tests.base import (
    mock_setup,
    DEVICE_BUILD_PAIRING,
)


class ShipperDeviceTestCase(TestCase):
    def setUp(self):
        mock_setup()

    def test_device_string(self):
        for device in Device.objects.all():
            self.assertEqual(
                str(device), f"{device.manufacturer} {device.name} ({device.codename})"
            )


class ShipperBuildTestCase(TestCase):
    def setUp(self):
        mock_setup()

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
        mock_setup()

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
                device.codename in DEVICE_BUILD_PAIRING
                and variant in DEVICE_BUILD_PAIRING[device.codename]
            ):
                build_count = DEVICE_BUILD_PAIRING[device.codename][variant]
            else:
                build_count = 0
            self.assertEqual(
                len(
                    device.get_all_enabled_hashed_builds_of_variant(
                        variant_codename=variant
                    )
                ),
                build_count,
            )
