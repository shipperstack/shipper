import ast

from django import template
from constance import config
from shipper.models import Build
from shipper.views import get_humanized_total_size

register = template.Library()


@register.inclusion_tag("admin_stats_variant_row.html")
def admin_stats_variant_row(variant):
    variants = ast.literal_eval(config.SHIPPER_UPLOAD_VARIANTS)
    return {
        "variant_name": variants[variant],
        "variant_builds_count": Build.objects.filter(variant=variant).count(),
        "variant_builds_size": get_humanized_total_size(
            Build.objects.filter(variant=variant)
        ),
    }
