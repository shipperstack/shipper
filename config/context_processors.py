from django.conf import settings


def download_page_processor(_):
    return {
            'main_website_url': settings.SHIPPER_MAIN_WEBSITE_URL,
            'downloads_page_main_branding': settings.SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING,
            'downloads_page_donation_url': settings.SHIPPER_DOWNLOADS_PAGE_DONATION_URL,
            'downloads_page_donation_message': settings.SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE,
            'upload_variants': settings.SHIPPER_UPLOAD_VARIANTS,
    }


def version_processor(_):
    return {'SHIPPER_VERSION': settings.SHIPPER_VERSION}


def debug_mode_processor(_):
    return {'DEBUG': settings.DEBUG}
