from django.test import TestCase

from shipper.models import Device, Build


class DeviceTestCase(TestCase):
    def setUp(self):
        mock_devices_setup()

    def test_device_string(self):
        bullhead = Device.objects.get(codename="bullhead")
        angler = Device.objects.get(codename="angler")
        dream2lte = Device.objects.get(codename="dream2lte")
        self.assertEqual(str(bullhead), "LG Nexus 5X (bullhead)")
        self.assertEqual(str(angler), "Huawei Nexus 6P (angler)")
        self.assertEqual(str(dream2lte), "Samsung Galaxy S8+ (dream2lte)")

    def test_image_url(self):
        bullhead = Device.objects.get(codename="bullhead")
        angler = Device.objects.get(codename="angler")
        dream2lte = Device.objects.get(codename="dream2lte")
        self.assertEqual(bullhead.get_photo_url(), "https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg")
        self.assertEqual(angler.get_photo_url(), "https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg")
        self.assertEqual(dream2lte.get_photo_url(), "#")


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
        bullhead = Device.objects.get(codename="bullhead")
        angler = Device.objects.get(codename="angler")
        dream2lte = Device.objects.get(codename="dream2lte")
        self.assertEqual(len(bullhead.get_all_gapps_build_objects()), 1)
        self.assertEqual(len(angler.get_all_gapps_build_objects()), 0)
        self.assertEqual(len(dream2lte.get_all_gapps_build_objects()), 1)


def mock_devices_setup():
    Device.objects.create(
        name="Nexus 5X",
        codename="bullhead",
        manufacturer="LG",
        photo="https://fdn2.gsmarena.com/vv/bigpic/lg-nexus-5x-.jpg",
        status=True
    )
    Device.objects.create(
        name="Nexus 6P",
        codename="angler",
        manufacturer="Huawei",
        photo="https://fdn2.gsmarena.com/vv/bigpic/huawei-nexus-6p-.jpg",
        status=False
    )
    Device.objects.create(
        name="Galaxy S8+",
        codename="dream2lte",
        manufacturer="Samsung",
        status=True
    )


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
        zip_file="bullhead/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip",
        md5_file="bullhead/Bliss-v14-dream2lte-OFFICIAL-gapps-20200609.zip.md5",
    )
    Build.objects.create(
        device=Device.objects.get(codename="angler"),
        file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608",
        size=857483855,
        version="v14",
        sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
        variant="vanilla",
        zip_file="bullhead/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip",
        md5_file="bullhead/Bliss-v14-angler-OFFICIAL-vanilla-20200608.zip.md5",
    )
