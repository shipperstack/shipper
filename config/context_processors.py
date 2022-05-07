import ast

from django.conf import settings
from constance import settings as csettings


def download_page_processor(_):
    variants = ast.literal_eval(csettings.SHIPPER_UPLOAD_VARIANTS)
    return {
        "main_website_url": csettings.SHIPPER_MAIN_WEBSITE_URL,
        "downloads_page_main_branding": csettings.SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING,
        "downloads_page_donation_url": csettings.SHIPPER_DOWNLOADS_PAGE_DONATION_URL,
        "downloads_page_donation_message": csettings.SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE,  # noqa: E501
        "upload_variants": variants,
    }


def version_processor(_):
    return {"SHIPPER_VERSION": settings.SHIPPER_VERSION}


def debug_mode_processor(_):
    return {"DEBUG": settings.DEBUG}
