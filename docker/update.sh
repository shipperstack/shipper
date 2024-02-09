#!/usr/bin/env bash
# Before running this file, fetch changes using git!

# Source activate alias file
. ./activate

# Set latest version tag
setlatest

# Check if version has been uploaded to GitHub Registry
if ! docker pull ghcr.io/shipperstack/shipper-server:${VERSION_TAG} > /dev/null ; then
    echo "The version hasn't been published yet! Try running the updater later."
    exit 1
fi

# Start Docker images
docker-compose up -d --no-build

# Migrate database, compile translations, and collect static files
./server-update.sh
