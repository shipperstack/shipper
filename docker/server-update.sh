#!/usr/bin/env bash

# Check developer argument
if [ "$#" == 1 ]; then
    if [ "$1" = "developer" ]; then
        developer=true
    else
        developer=false
    fi
else
    developer=false
fi

# Execute commands based on developer flag
if [ "$developer" = true ]; then
    echo "Using developer docker-compose file..."
    docker compose -f docker-compose.dev.yml exec web python3 manage.py migrate --noinput
    docker compose -f docker-compose.dev.yml exec web python3 manage.py compilemessages
    docker compose -f docker-compose.dev.yml exec web python3 manage.py collectstatic --no-input --clear
else
    echo "Using production docker-compose file..."
    docker compose exec web python3 manage.py migrate --noinput
    docker compose exec web python3 manage.py compilemessages
    docker compose exec web python3 manage.py collectstatic --no-input --clear
fi
