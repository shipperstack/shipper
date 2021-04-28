from django.conf import settings


def version_processor(request):
    return {'SHIPPER_VERSION': settings.SHIPPER_VERSION}
