import os
import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy
from kombu import Queue, Exchange
from paramiko import AuthenticationException, SSHException
from billiard.exceptions import TimeLimitExceeded
from sentry_sdk.integrations.django import DjangoIntegration
from pathlib import Path
from dotenv import load_dotenv

from .filters import IgnoreMissingBuild503Errors
from core.exceptions import UploadException, BuildMirrorException

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SHIPPER_SECRET_KEY")
DEBUG = int(os.environ.get("SHIPPER_DEBUG", default=0))
try:
    ALLOWED_HOSTS = os.environ.get("SHIPPER_ALLOWED_HOSTS").split(" ")
except AttributeError:
    # Check will catch this error
    pass

try:
    CSRF_TRUSTED_ORIGINS = os.environ.get("SHIPPER_CSRF_TRUSTED_ORIGINS").split(" ")
except AttributeError:
    # Check will catch this error
    pass

CSRF_COOKIE_SECURE = int(os.environ.get("SHIPPER_CSRF_COOKIE_SECURE", default=1))
SESSION_COOKIE_SECURE = int(os.environ.get("SHIPPER_SESSION_COOKIE_SECURE", default=1))

SECURE_HSTS_SECONDS = int(os.environ.get("SHIPPER_SECURE_HSTS_SECONDS", default=0))

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


with open("version.txt") as v_file:
    SHIPPER_VERSION = v_file.readline().rstrip()

with open("shippy_compat_version.txt") as v_file:
    SHIPPER_SHIPPY_COMPAT_VERSION = v_file.readline().rstrip()


# Application definition
INSTALLED_APPS = [
    "constance",
    "django.contrib.admin",
    "django.contrib.auth",
    "accounts",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "core",
    "downloads",
    "maintainers",
    "api",
    "internaladmin",
    "drf_chunked_upload",
    "auditlog",
    "django_celery_beat",
    "django_celery_results",
    "crispy_forms",
    "crispy_bootstrap5",
    "dbbackup",
    "django_cleanup.apps.CleanupConfig",  # must be last for successful deletions
]

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
    "config.middleware.SetIPMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.download_page_processor",
                "config.context_processors.version_processor",
                "config.context_processors.debug_mode_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
SQL_ENGINE = os.environ.get("SHIPPER_SQL_ENGINE", default="django.db.backends.sqlite3")
SQL_DB_NAME = os.environ.get("SHIPPER_SQL_DATABASE")
if SQL_ENGINE == "django.db.backends.sqlite3":
    SQL_DB_NAME = str(BASE_DIR / f"{SQL_DB_NAME}.sqlite3")
DATABASES = {
    "default": {
        "ENGINE": SQL_ENGINE,
        "NAME": SQL_DB_NAME,
        "USER": os.environ.get("SHIPPER_SQL_USER", default="user"),
        "PASSWORD": os.environ.get("SHIPPER_SQL_PASSWORD", default="password"),
        "HOST": os.environ.get("SHIPPER_SQL_HOST", default="localhost"),
        "PORT": os.environ.get("SHIPPER_SQL_PORT", default="5432"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{name}"}
    for name in [
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    ]
]


# Cache
CACHES = {
    "default": {
        "BACKEND": os.environ.get(
            "SHIPPER_CACHE_BACKEND",
            default="django.core.cache.backends.locmem.LocMemCache",
        ),
        "LOCATION": os.environ.get("SHIPPER_CACHE_LOCATION", default="shipper-cache"),
    }
}
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 30
CACHE_MIDDLEWARE_KEY_PREFIX = "shipper"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "ignore_missing_build_503_errors": {
            "()": IgnoreMissingBuild503Errors,
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true", "ignore_missing_build_503_errors"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "filters": ["ignore_missing_build_503_errors"],
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false", "ignore_missing_build_503_errors"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Email
EMAIL_BACKEND = os.environ.get(
    "SHIPPER_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("SHIPPER_EMAIL_HOST", default="")
EMAIL_PORT = os.environ.get("SHIPPER_EMAIL_PORT", default="")
EMAIL_HOST_USER = os.environ.get("SHIPPER_EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = os.environ.get("SHIPPER_EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = int(os.environ.get("SHIPPER_EMAIL_USE_TLS", default=1))
DEFAULT_FROM_EMAIL = os.environ.get("SHIPPER_DEFAULT_FROM_EMAIL", default="")

ADMINS = [
    tuple(i.split(":"))
    for i in os.environ.get("SHIPPER_ADMIN_EMAILS", default="").split(";")
]
MANAGERS = ADMINS

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("ko", gettext_lazy("Korean")),
    ("en", gettext_lazy("English")),
]

LOCALE_PATHS = (BASE_DIR / "locale",)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Login
LOGIN_REDIRECT_URL = "/maintainers/"

# Storage
STORAGES = {
    "dbbackup": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": os.environ.get(
                "SHIPPER_DBBACKUP_DIRECTORY", default="/tmp/shipper-backup/"
            ),
        },
    },
}

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "10/minute", "user": "10/second"},
}


# drf-chunked-upload
DRF_CHUNKED_UPLOAD_COMPLETE_EXT = ""
DRF_CHUNKED_UPLOAD_ABSTRACT_MODEL = False
DRF_CHUNKED_UPLOAD_CHECKSUM = os.environ.get(
    "SHIPPER_UPLOAD_CHECKSUM", default="sha256"
)
DRF_CHUNKED_UPLOAD_MAX_BYTES = 5_000_000_000  # 5 GB


# Celery
CELERY_BROKER_URL = "pyamqp://rabbitmq:5672/"
CELERY_TASK_TIME_LIMIT = 60 * int(os.environ.get("SHIPPER_TASK_TIME_LIMIT", default=60))
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_CACHE = "default"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_EXTENDED = True
CELERY_DEFAULT_QUEUE = "default"
CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("mirror_upload", Exchange("mirror_upload"), routing_key="mirror_upload"),
)


# Constance
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "SHIPPER_MAIN_WEBSITE_URL": (
        "#",
        "Link to redirect users to when they click on the 'Back to main website' "
        "button on the top of the page. Setting this configuration to the pound "
        "symbol disables redirection and hides the button.",
        str,
    ),
    "SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING": (
        "Downloads",
        "Sets the navbar branding at the top left of the website.",
        str,
    ),
    "SHIPPER_DOWNLOADS_PAGE_DONATION_URL": (
        "#",
        "URL to refer users to when they wish to donate.",
        str,
    ),
    "SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE": (
        "Please consider donating, thank you!",
        "Donation message to show to users in the donation banner.",
        str,
    ),
    "SHIPPER_DOWNLOADS_DISABLE_MAIN_SERVER": (
        False,
        "Disables downloads from the main server. Enable only if you are experiencing "
        "load problems.",
        bool,
    ),
    "SHIPPER_DOWNLOADS_ARCHIVE_THROTTLE": (
        1,
        "Throttles the download speed of archived builds, in MB/s.",
        int,
    ),
    "SHIPPER_FILE_NAME_FORMAT": (
        "[A-Za-z]+-(?P<version>[a-z0-9.]+)-(?P<codename>[A-Za-z0-9_]+)-OFFICIAL-("
        "?P<variant>[a-z]+)-(?P<date>[0-9]{8}).zip",
        "Regex pattern to use when parsing file names of uploaded artifacts. The "
        "pattern must include the following four named match groups; otherwise an "
        "exception will occur during uploading: `version', `codename`, `variant`, "
        "and `date`.",
        str,
    ),
    "SHIPPER_ALLOWED_VERSIONS_TO_UPLOAD": (
        "*",
        "Versions that maintainers can currently upload to the system. Wildcards are "
        "supported. Specify multiple versions on each line.",
        str,
    ),
    "SHIPPER_BUILD_ARCHIVE_DAYS": (
        90,
        "Builds that are 'archived' in the system after this many number of days. "
        "Archived builds are not mirrored to any mirror servers.",
        int,
    ),
    "SHIPPER_ENABLE_MIRRORING": (
        True,
        "Enables the mirroring functionality of shipper. Disable temporarily if you "
        "are experiencing problems.",
        bool,
    ),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "Downloads page": (
        "SHIPPER_MAIN_WEBSITE_URL",
        "SHIPPER_DOWNLOADS_PAGE_MAIN_BRANDING",
        "SHIPPER_DOWNLOADS_PAGE_DONATION_URL",
        "SHIPPER_DOWNLOADS_PAGE_DONATION_MESSAGE",
    ),
    "Download": (
        "SHIPPER_DOWNLOADS_DISABLE_MAIN_SERVER",
        "SHIPPER_DOWNLOADS_ARCHIVE_THROTTLE",
    ),
    "Upload": (
        "SHIPPER_FILE_NAME_FORMAT",
        "SHIPPER_ALLOWED_VERSIONS_TO_UPLOAD",
    ),
    "Maintenance": ("SHIPPER_BUILD_ARCHIVE_DAYS",),
    "Mirroring": ("SHIPPER_ENABLE_MIRRORING",),
}

# django-auditlog
AUDITLOG_INCLUDE_TRACKING_MODELS = ("constance.Constance",)

# Django Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# django-ipware
IPWARE_META_PRECEDENCE_ORDER = (
    "HTTP_CF_CONNECTING_IP",
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
)


# Sentry SDK
def before_send(event, hint):
    if "log_record" in hint:
        if hint["log_record"].name == "django.security.DisallowedHost":
            return None
    return event


if DEBUG == 1:
    sentry_transaction_rate = 1.0
else:
    sentry_transaction_rate = 0.2


sentry_sdk.init(
    dsn=os.environ.get("SHIPPER_SENTRY_SDK_DSN", default=""),
    integrations=[DjangoIntegration()],
    release=f"{SHIPPER_VERSION}",
    traces_sample_rate=sentry_transaction_rate,
    send_default_pii=(int(os.environ.get("SHIPPER_SENTRY_SDK_PII", default=0)) == 0),
    before_send=before_send,
    ignore_errors=[
        SSHException,
        AuthenticationException,
        ConnectionRefusedError,
        TimeLimitExceeded,
        KeyboardInterrupt,
        UploadException,
        BuildMirrorException,
        ImproperlyConfigured,
    ],
)
