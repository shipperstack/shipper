from django import template

register = template.Library()


def format_download_url(value, arg):
    """Formats download URL with file name"""
    return value.format(arg)


register.filter('format_download_url', format_download_url)
