#!/usr/bin/env bash

# Fetch latest docker-compose file
curl https://raw.githubusercontent.com/ericswpark/shipper/master/docker-compose.yml > docker-compose.yml

# Fetch latest nginx configuration
curl https://raw.githubusercontent.com/ericswpark/shipper/master/nginx/nginx.conf > nginx/nginx.conf

# Fetch latest activation script
curl https://raw.githubusercontent.com/ericswpark/shipper/master/activate > activate

# Fetch Django migration/static file collection script
curl https://raw.githubusercontent.com/ericswpark/shipper/master/django-update.sh > django-update.sh
chmod +x django-update.sh

# Source activate alias file
. ./activate

# Set latest version tag
setlatest

# Start Docker images
docker-compose up -d --no-build

# Migrate database, compile translations, and collect static files
./django-update.sh

