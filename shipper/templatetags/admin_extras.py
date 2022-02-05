from django import template

from config import settings

from shipper.views import get_humanized_total_size
from shipper.models import Build

register = template.Library()


@register.inclusion_tag('admin_stats_variant_row.html')
def admin_stats_variant_row(variant):
    return {
        'variant_name': settings.SHIPPER_UPLOAD_VARIANTS[variant],
        'variant_builds_count': Build.objects.filter(variant=variant).count(),
        'variant_builds_size': get_humanized_total_size(Build.objects.filter(variant=variant)),
    }
