import ast

from django.conf import settings
from constance import config


def download_page_processor(_):
    variants = ast.literal_eval(config.SHIPPER_UPLOAD_VARIANTS)
    return {
        "main_website_url": config.SHIPPER_MAIN_WEBSITE_URL,
        "downloads_page_main_branding": config.SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING,
        "downloads_page_donation_url": config.SHIPPER_DOWNLOADS_PAGE_DONATION_URL,
        "downloads_page_donation_message": config.SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE,  # noqa: E501
        "downloads_disable_main_server": config.SHIPPER_DOWNLOADS_DISABLE_MAIN_SERVER,
        "upload_variants": variants,
    }


def version_processor(_):
    return {"SHIPPER_VERSION": settings.SHIPPER_VERSION}


def debug_mode_processor(_):
    return {"DEBUG": settings.DEBUG}
