import datetime

from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import v1_download_count_day, v1_download_count_week, v1_download_count_month, v1_download_count_all, \
    v1_download_build_counter
from shipper.models import Statistics, Build
from shipper.tests import mock_devices_setup, mock_builds_setup


class StatisticsTestCase(APITestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        mock_statistics_setup()
        self.factory = APIRequestFactory()

    def test_v1_download_count_day(self):
        request = self.factory.get("/api/v1/download/count/day/")
        request.user = AnonymousUser()
        response = v1_download_count_day(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 700)

    def test_v1_download_count_week(self):
        request = self.factory.get("/api/v1/download/count/week/")
        request.user = AnonymousUser()
        response = v1_download_count_week(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1900)

    def test_v1_download_count_month(self):
        request = self.factory.get("/api/v1/download/count/month/")
        request.user = AnonymousUser()
        response = v1_download_count_month(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2100)

    def test_v1_download_count_all(self):
        request = self.factory.get("/api/v1/download/count/all/")
        request.user = AnonymousUser()
        response = v1_download_count_all(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2100)


class StatisticsIncrementTestCase(APITestCase):
    def setUp(self):
        mock_devices_setup()
        mock_builds_setup()
        mock_statistics_setup()
        self.factory = APIRequestFactory()

    def test_v1_download_build_counter(self):
        request = self.factory.post("/api/v1/download/build/counter/", data={
            "file_name": "Bliss-v14-angler-OFFICIAL-vanilla-20200608"
        })
        request.user = AnonymousUser()
        response = v1_download_build_counter(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Build.objects.get(file_name="Bliss-v14-angler-OFFICIAL-vanilla-20200608").download_count, 61)


def mock_statistics_setup():
    Statistics.objects.create(
        date=datetime.date.today(),
        download_count=500,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=1),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=2),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=3),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=4),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=5),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=6),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=7),
        download_count=200,
    )
    Statistics.objects.create(
        date=datetime.date.today()-datetime.timedelta(days=21),
        download_count=200,
    )
