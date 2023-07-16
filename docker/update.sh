#!/usr/bin/env bash
# Before running this file, fetch changes using git!

# Source activate alias file
. ./activate

# Set latest version tag
setlatest

# Start Docker images
docker-compose up -d --no-build

# Migrate database, compile translations, and collect static files
./server-update.sh
