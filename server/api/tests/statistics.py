import datetime

from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import (
    v1_download_count_day,
    v1_download_count_week,
    v1_download_count_month,
    v1_download_count_all,
    V2DownloadBuildCounter,
)
from core.models import Statistics, Build
from core.tests.base import mock_setup


class StatisticsTestCase(APITestCase):
    def setUp(self):
        mock_setup()
        mock_statistics_setup()
        self.factory = APIRequestFactory()

    def test_v1_download_count_day(self):
        request = self.factory.get("/api/v1/download/count/day/")
        request.user = AnonymousUser()
        response = v1_download_count_day(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_v1_download_count_week(self):
        request = self.factory.get("/api/v1/download/count/week/")
        request.user = AnonymousUser()
        response = v1_download_count_week(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_v1_download_count_month(self):
        request = self.factory.get("/api/v1/download/count/month/")
        request.user = AnonymousUser()
        response = v1_download_count_month(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 4)

    def test_v1_download_count_all(self):
        request = self.factory.get("/api/v1/download/count/all/")
        request.user = AnonymousUser()
        response = v1_download_count_all(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)


class StatisticsIncrementTestCase(APITestCase):
    def setUp(self):
        mock_setup()
        mock_statistics_setup()
        self.factory = APIRequestFactory()
        V2DownloadBuildCounter.throttle_classes = ()

    def test_v2_download_build_counter(self):
        previous_count = Build.objects.get(
            file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608"
        ).build_stats.count()
        request = self.factory.post(
            "/api/v2/download/build/counter/",
            data={
                "file_name": "Bliss-v14-angler-OFFICIAL-vanilla-20200608",
                "download_type": "download",
            },
        )
        request.user = AnonymousUser()
        response = V2DownloadBuildCounter.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Build.objects.get(
                file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608"
            ).build_stats.count()
            > previous_count
        )

    def test_v2_download_build_counter_invalid_build_name(self):
        request = self.factory.post(
            "/api/v2/download/build/counter/",
            data={
                "file_name": "Bliss-v14-unknown-OFFICIAL-vanilla-20200608",
                "download_type": "download",
            },
        )
        request.user = AnonymousUser()
        response = V2DownloadBuildCounter.as_view()(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "invalid_build_name")

    def test_v2_download_build_counter_invalid_build_id(self):
        request = self.factory.post(
            "/api/v2/download/build/counter/",
            data={
                "build_id": 999999999,
                "download_type": "download",
            },
        )
        request.user = AnonymousUser()
        response = V2DownloadBuildCounter.as_view()(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "invalid_build_id")

    def test_v2_download_build_counter_invalid_download_type(self):
        request = self.factory.post(
            "/api/v2/download/build/counter/",
            data={
                "file_name": "Bliss-v14-angler-OFFICIAL-vanilla-20200608",
                "download_type": "invalid",
            },
        )
        request.user = AnonymousUser()
        response = V2DownloadBuildCounter.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "invalid_download_type")

    def test_v2_download_build_counter_missing_build_information(self):
        request = self.factory.post(
            "/api/v2/download/build/counter/",
            data={
                "download_type": "download",
            },
        )
        request.user = AnonymousUser()
        response = V2DownloadBuildCounter.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "missing_build_information")


def mock_statistics_object_create(time, build, ip):
    new_stat = Statistics.objects.create(build=build, ip=ip)
    new_stat.time = time
    new_stat.save()


def mock_statistics_setup():
    mock_statistics_object_create(
        time=timezone.now() - datetime.timedelta(days=1),
        build=Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"),
        ip="127.0.0.1",
    )
    mock_statistics_object_create(
        time=timezone.now() - datetime.timedelta(days=3),
        build=Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"),
        ip="127.0.0.1",
    )
    mock_statistics_object_create(
        time=timezone.now() - datetime.timedelta(days=5),
        build=Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"),
        ip="127.0.0.1",
    )
    mock_statistics_object_create(
        time=timezone.now() - datetime.timedelta(days=9),
        build=Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"),
        ip="127.0.0.1",
    )
    mock_statistics_object_create(
        time=timezone.now() - datetime.timedelta(days=31),
        build=Build.objects.get(file_name="Bliss-v14-bullhead-OFFICIAL-gapps-20200608"),
        ip="127.0.0.1",
    )
