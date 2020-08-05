# shipper

Artifact release manager with API support and user presentation

This system was designed to replace our aging downloads infrastructure.

## Important

Before deploying live, remember to change the `SECRET_KEY` value in `config/settings.py`!

## Quickstart

Make sure Python 3 and pip are installed.

Shipper depends on RabbitMQ. Install RabbitMQ using your package manager.

For production environments, we recommend using `supervisord`.

    pip install -r requirements.txt     # install dependencies
    python manage.py migrate            # create initial db
    python manage.py runserver          # run internal webserver
    celery -A shipper worker -l info    # run Celery

## Running in production

If your configuration file has different values, sometimes pulling the latest changes may result in a conflict.

To fix this, stash the changes first, pull, then pop the stash.

    git stash
    git pull
    git stash pop

If you are using `supervisorctl`, then the following commands may help.

    sudo supervisorctl restart shipper
    sudo supervisorctl restart shipper-celery
    sudo supervisorctl status

If there are new dependencies, remember to source the virtual environment and then download the latest dependencies.