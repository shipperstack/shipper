from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from core.tests.base import mock_setup
from django.contrib.auth import get_user_model

from internaladmin.views import (
    AdminBuildMirrorStatusView,
    AdminStatisticsView,
    get_humanized_total_size,
)

User = get_user_model()


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


class InternalAdminViewTestCase(TestCase):
    def setUp(self):
        mock_setup()
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@example.com", password="password"
        )
        self.client.force_login(user=self.user)

    def test_admin_statistics_view(self):
        request = self.factory.get("")
        request.user = self.user
        response = AdminStatisticsView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_admin_statistics_view_no_permissions(self):
        request = self.factory.get("")
        request.user = AnonymousUser()
        response = AdminStatisticsView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_admin_mirror_status_view(self):
        request = self.factory.get("")
        request.user = self.user
        response = AdminBuildMirrorStatusView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_admin_mirror_status_view_no_permissions(self):
        request = self.factory.get("")
        request.user = AnonymousUser()
        response = AdminBuildMirrorStatusView.as_view()(request)

        self.assertEqual(response.status_code, 302)
