from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BuildAttributeFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return [
            ("true", _("Yes")),
            ("false", _("No")),
        ]


class BuildHashedFilter(BuildAttributeFilter):
    title = _("hashed")
    parameter_name = "hashed"

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        ids = []

        if self.value() == "true":
            ids = [build.id for build in queryset.all() if build.is_hashed()]
        elif self.value() == "false":
            ids = [build.id for build in queryset.all() if not build.is_hashed()]

        return queryset.filter(id__in=ids)


class BuildMirroredFilter(BuildAttributeFilter):
    title = _("mirrored")
    parameter_name = "mirrored"

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        ids = []

        if self.value() == "true":
            ids = [build.id for build in queryset.all() if build.is_mirrored()]
        elif self.value() == "false":
            ids = [build.id for build in queryset.all() if not build.is_mirrored()]

        return queryset.filter(id__in=ids)


class BuildArchivedFilter(BuildAttributeFilter):
    title = _("archived")
    parameter_name = "archived"

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        ids = []

        if self.value() == "true":
            ids = [build.id for build in queryset.all() if build.is_archived()]
        elif self.value() == "false":
            ids = [build.id for build in queryset.all() if not build.is_archived()]

        return queryset.filter(id__in=ids)
