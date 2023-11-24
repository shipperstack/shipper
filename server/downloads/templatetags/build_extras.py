from django import template
from core.models import Variant

register = template.Library()


@register.filter
def format_download_url(value, arg):
    """Formats download URL with file name"""
    return value.format(arg)


@register.inclusion_tag("downloads_device_variant.html")
def device_variant_section(device, variant):
    variants = {}
    for v in Variant.objects.all():
        variants[v.codename] = v.description
    return {
        "device": device,
        "variant_name": variants[variant],
        "build_objects": device.get_all_enabled_hashed_builds_of_variant(
            variant_codename=variant
        ),
    }
