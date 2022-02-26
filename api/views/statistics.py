import datetime

from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from shipper.models import Build, Statistics

from .utils import get_client_ip


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
                Statistics.objects.create(device=build.device, build=build, ip=get_client_ip(request=request))
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
                Statistics.objects.create(device=build.device, build=build, ip=get_client_ip(request=request))
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
    return Statistics.objects.all().count()


def download_count_by_days_response(days):
    return Statistics.objects.filter(time__gte=django.util.timezone.now() - datetime.timedelta(days=days)).count()
