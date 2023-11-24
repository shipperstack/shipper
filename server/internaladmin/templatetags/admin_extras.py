from django import template

from internaladmin.views import get_humanized_total_size
from core.models import Build, Variant

register = template.Library()


@register.inclusion_tag("admin_stats_variant_row.html")
def admin_stats_variant_row(variant):
    variants = {}
    for variant in Variant.objects.all():
        variants[variant.codename] = variant.description
    return {
        "variant_name": variants[variant],
        "variant_builds_count": Build.objects.filter(variant__codename=variant).count(),
        "variant_builds_size": get_humanized_total_size(
            Build.objects.filter(variant=variant)
        ),
    }
