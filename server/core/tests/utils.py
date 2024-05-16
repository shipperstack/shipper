from django.test import TestCase, override_settings

from core.utils import is_version_in_target_versions, parse_filename_with_regex
from core.exceptions import UploadException


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
        with self.assertRaisesRegex(Exception, "version-has-wildcard"):
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
