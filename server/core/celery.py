import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize the configuration
# object to child processes.
# `namespace='CELERY'` means all celery-related configuration keys should have a
# `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "mirror_build_async_result_cleanup": {
        "task": "mirror_build_async_result_cleanup",
        "schedule": 60 * 5,  # Every 5 minutes
    },
    "process_incomplete_builds": {
        "task": "process_incomplete_builds",
        "schedule": 60 * 60 * 1,  # Every 1 hour
    },
    "device_photo_download": {
        "task": "device_photo_download",
        "schedule": 60 * 5,  # Every 5 minutes
    },
    "device_photo_thumbhash_generate": {
        "task": "device_photo_thumbhash_generate",
        "schedule": 60 * 5,  # Every 5 minutes
    },
    "drf_chunked_upload_cleanup": {
        "task": "drf_chunked_upload_cleanup",
        "schedule": 60 * 60 * 24 * 7,  # Every week
    },
}
