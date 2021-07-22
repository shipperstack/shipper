from django.test import TestCase

from downloads.templatetags.build_extras import format_download_url


class ShipperTemplateTagsTestCase(TestCase):
    def test_format_download_url(self):
        self.assertEqual("https://mock/test/Bliss-v14.zip/download/",
                         format_download_url("https://mock/test/{}/download/", "Bliss-v14.zip"))
