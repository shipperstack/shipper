from django.urls import path

from api.views import (
    v1_maintainers_login,
    v1_maintainers_token_check,
    v1_maintainers_build_duplicate_check,
    v1_maintainers_upload_filename_regex_pattern,
    V1MaintainersChunkedUpload,
    v1_maintainers_build_enabled_status_modify,
)

urlpatterns = [
    path("maintainers/login/", v1_maintainers_login, name="v1_maintainers_login"),
    path(
        "maintainers/token_check/",
        v1_maintainers_token_check,
        name="v1_maintainers_token_check",
    ),
    path(
        "maintainers/build/duplicate_check/",
        v1_maintainers_build_duplicate_check,
        name="v1_maintainers_build_duplicate_check",
    ),
    path(
        "maintainers/upload_filename_regex_pattern/",
        v1_maintainers_upload_filename_regex_pattern,
        name="v1_maintainers_upload_filename_regex_pattern",
    ),
    path(
        "maintainers/chunked_upload/",
        V1MaintainersChunkedUpload.as_view(),
        name="v1_maintainers_chunked_upload",
    ),
    path(
        "maintainers/chunked_upload/<uuid:pk>/",
        V1MaintainersChunkedUpload.as_view(),
        name="v1_maintainers_chunked_upload_detail",
    ),
    path(
        "maintainers/build/enabled_status_modify/",
        v1_maintainers_build_enabled_status_modify,
        name="v1_maintainers_build_enabled_status_modify",
    ),
]
