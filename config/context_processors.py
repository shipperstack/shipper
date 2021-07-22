from django.conf import settings


def download_page_processor(request):
    return {
            'main_website_url': settings.SHIPPER_MAIN_WEBSITE_URL,
            'downloads_page_main_branding': settings.SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING,
            'downloads_page_donation_url': settings.SHIPPER_DOWNLOADS_PAGE_DONATION_URL,
            'downloads_page_donation_message': settings.SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE
    }


def version_processor(request):
    return {'SHIPPER_VERSION': settings.SHIPPER_VERSION}


def debug_mode_processor(request):
    return {'DEBUG': settings.DEBUG}
