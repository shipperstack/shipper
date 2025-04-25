from django.test import TestCase

from internaladmin.views import get_humanized_total_size


class MockBuild:
    def __init__(self, size):
        self.size = size


class InternalAdminHelperTestCase(TestCase):
    def test_humanize(self):
        build_list = [
            MockBuild(1024),
            MockBuild(231851),
        ]
        self.assertEqual(get_humanized_total_size(build_list), "232.9 kB")
