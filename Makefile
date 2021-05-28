.PHONY: usage up down restart setup dup ddown drestart dsetup test testreport

usage:
	echo "Use up/down/restart for production, dup/ddown/drestart for development"

up:
	docker-compose up -d

down:
	docker-compose down

restart: down up

setup:
	docker-compose exec web python3 manage.py migrate --noinput
	docker-compose exec web python3 manage.py collectstatic --no-input --clear

dup:
	docker-compose -f docker-compose.dev.yml up -d --build

ddown:
	docker-compose -f docker-compose.dev.yml down

drestart: ddown dup

dsetup:
	docker-compose -f docker-compose.dev.yml exec web python3 manage.py migrate --noinput
	docker-compose -f docker-compose.dev.yml exec web python3 manage.py collectstatic --no-input --clear
