import datetime

from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from shipper.models import Build, Statistics


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def v1_download_build_counter(request):
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


def build_increase_download_count(build):
    build.download_count += 1
    build.save()

    # Increase overall statistics
    try:
        stats = Statistics.objects.get(date=datetime.date.today())
    except Statistics.DoesNotExist:
        stats = Statistics.objects.create()

    stats.download_count += 1
    stats.save()
