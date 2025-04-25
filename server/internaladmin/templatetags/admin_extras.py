from django import template

from internaladmin.views import get_humanized_total_size
from core.models import Build, Variant

register = template.Library()


@register.inclusion_tag("admin_stats_variant_row.html")
def admin_stats_variant_row(variant_codename):
    variant = Variant.objects.get(codename=variant_codename)

    return {
        "variant_name": variant.description,
        "variant_builds_count": Build.objects.filter(
            variant__codename=variant_codename
        ).count(),
        "variant_builds_size": get_humanized_total_size(
            Build.objects.filter(variant=variant)
        ),
    }
