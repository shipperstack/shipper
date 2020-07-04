# shipper

Artifact release manager with API support and user presentation

This system was designed to replace our aging downloads infrastructure.

## Important

Before deploying live, remember to change the `SECRET_KEY` value in `config/settings.py`!

## Quickstart

Make sure Python 3 and pip are installed.

Shipper depends on RabbitMQ. Install RabbitMQ using your package manager.

    pip install -r requirements.txt     # install dependencies
    python manage.py migrate            # create initial db
    python manage.py runserver          # run internal webserver
    celery -A shipper worker -l info    # run Celery
    