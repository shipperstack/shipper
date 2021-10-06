from django.test import TestCase


from shipper.exceptions import UploadException
from shipper.handler import file_name_validity_check
from shipper.models import Device, Build


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
        self.assertEqual(len(build.get_enabled_downloadable_mirrors()), 0)


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
    Build.objects.create(
        device=Device.objects.get(codename="bullhead"),
        file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="gapps",
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
        zip_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip",
        md5_file="angler/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip.md5",
        download_count=60,
    )
