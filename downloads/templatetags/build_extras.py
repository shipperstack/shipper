import ast

from django import template
from constance import settings

register = template.Library()


@register.filter
def format_download_url(value, arg):
    """Formats download URL with file name"""
    return value.format(arg)


@register.inclusion_tag("downloads_device_variant.html")
def device_variant_section(device, variant):
    variants = ast.literal_eval(settings.SHIPPER_UPLOAD_VARIANTS)
    return {
        "device": device,
        "variant_name": variants[variant],
        "build_objects": device.get_all_enabled_hashed_builds_of_variant(
            variant=variant
        ),
    }
