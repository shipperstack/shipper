from django import template

register = template.Library()


@register.simple_tag
def format_download_url(value, arg):
    """Formats download URL with file name"""
    return value.format(arg)
