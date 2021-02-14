#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Uncomment this if you want your env to be reset on every restart
# Will make debugging extremely harder
# python manage.py flush --no-input

python manage.py migrate

exec "$@"