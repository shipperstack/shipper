#!/bin/bash

# Stop shipper instance
sudo supervisorctl stop shipper
sudo supervisorctl stop shipper-celery

# Change working directory
pushd /home/shipper

# Download new changes as shipper user
sudo -u shipper -H bash -c "git pull"

# Apply Django maintenance tasks
sudo -u shipper -H bash -c "source venv/bin/activate && python3 manage.py migrate && python manage.py collectstatic"

# Close working directory handle
popd

# Start shipper instance
sudo supervisorctl start shipper
sudo supervisorctl start shipper-celery