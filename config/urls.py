from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("maintainers/", include("maintainers.urls")),
    path("", include("downloads.urls")),
    path("internal-admin/", include("internaladmin.urls")),
    path("api/", include("api.urls")),
    path("", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
