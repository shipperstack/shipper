.PHONY: up down restart dup ddown drestart

up:
	docker-compose up -d

down:
	docker-compose down

restart: down up

dup:
	docker-compose -f docker-compose.dev.yml up -d --build

ddown:
	docker-compose -f docker-compose.dev.yml down

drestart: ddown dup
