import datetime

from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from shipper.models import Build, Statistics


class V1DownloadBuildCounter(APIView):
    """
    Endpoint to increment build download count
    """
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        file_name = request.data.get("file_name")

        if file_name:
            try:
                build = Build.objects.get(file_name=file_name)
                build_increase_download_count(build)
                return Response(
                    {
                        'message': 'The request was successful!'
                    },
                    status=HTTP_200_OK
                )
            except Build.DoesNotExist:
                return Response(
                    {
                        'error': 'invalid_build_name',
                        'message': 'A build with that file name does not exist!'
                    },
                    status=HTTP_404_NOT_FOUND
                )

        build_id = request.data.get("build_id")

        if build_id:
            try:
                build = Build.objects.get(pk=int(build_id))
                build_increase_download_count(build)
                return Response(
                    {
                        'message': 'The request was successful!'
                    },
                    status=HTTP_200_OK
                )
            except Build.DoesNotExist:
                return Response(
                    {
                        'error': 'invalid_build_id',
                        'message': 'A build with that ID does not exist!'
                    },
                    status=HTTP_404_NOT_FOUND
                )

        return Response(
            {
                'error': 'missing_parameters',
                'message': 'No parameters specified. Specify a file_name parameter or a build_id parameter.'
            },
            status=HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_download_count_day(_):
    return download_count_by_days_response(1)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_download_count_week(_):
    return download_count_by_days_response(7)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_download_count_month(_):
    return download_count_by_days_response(31)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def v1_download_count_all(_):
    # Get all objects
    stats = Statistics.objects.all()
    return download_count_response(stats)


def download_count_by_days_response(days):
    stats = Statistics.objects.filter(date__gte=datetime.date.today() - datetime.timedelta(days=days))
    return download_count_response(stats)


def download_count_response(stats):
    count = 0
    for stat in stats:
        count += stat.download_count

    return Response(
        {
            'count': count
        }, status=HTTP_200_OK
    )


def build_increase_download_count(build):
    Build.objects.select_for_update().filter(id=build.id).update(download_count=F('download_count') + 1)

    # Increase overall statistics
    try:
        stats = Statistics.objects.get(date=datetime.date.today())
    except Statistics.DoesNotExist:
        stats = Statistics.objects.create()

    Statistics.objects.select_for_update().filter(date=stats.date).update(download_count=F('download_count') + 1)
