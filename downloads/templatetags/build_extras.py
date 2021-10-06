from django import template

from config import settings

register = template.Library()


@register.filter
def format_download_url(value, arg):
    """Formats download URL with file name"""
    return value.format(arg)


@register.inclusion_tag('downloads_device_variant.html')
def device_variant_section(device, variant):
    return {
        'device': device,
        'variant_name': settings.SHIPPER_UPLOAD_VARIANTS[variant],
        'build_objects': device.get_all_build_objects_of_variant(variant=variant),
    }
