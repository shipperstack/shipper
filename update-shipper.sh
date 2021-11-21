#!/usr/bin/env bash

# Fetch latest docker-compose file
curl https://raw.githubusercontent.com/ericswpark/shipper/master/docker-compose.yml > docker-compose.yml

# Fetch latest nginx configuration
curl https://raw.githubusercontent.com/ericswpark/shipper/master/nginx/nginx.conf > nginx/nginx.conf

# Fetch latest activation script
curl https://raw.githubusercontent.com/ericswpark/shipper/master/activate > activate

# Source activate alias file
. activate

# Set latest version tag
setlatest

# Start Docker images
docker-compose up -d --no-build

# Migrate database and collect static files
docker-compose exec web python3 manage.py migrate --noinput
docker-compose exec web python3 manage.py collectstatic --no-input --clear

