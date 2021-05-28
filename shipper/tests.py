from django.test import TestCase

from shipper.models import Device


class DeviceTestCase(TestCase):
    def setUp(self):
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

    def test_device_string(self):
        bullhead = Device.objects.get(codename="bullhead")
        angler = Device.objects.get(codename="angler")
        self.assertEqual(str(bullhead), "LG Nexus 5X (bullhead)")
        self.assertEqual(str(angler), "Huawei Nexus 6P (angler)")

