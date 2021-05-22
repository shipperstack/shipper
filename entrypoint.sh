#!/bin/sh

if [ "$SHIPPER_SQL_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SHIPPER_SQL_HOST $SHIPPER_SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"