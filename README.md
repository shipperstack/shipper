# shipper

Artifact release manager with API support and user presentation

This system was designed to replace our aging downloads infrastructure.

## Installation

Please [check out the wiki for installing and configuring shipper.](wiki/Installation)

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

If there are database changes, remember to migrate:

    python3 manage.py migrate

You may also need to update static files:

    python3 manage.py collectstatic

