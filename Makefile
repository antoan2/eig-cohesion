build:
	docker-compose build

up-dev:
	docker-compose up -d

up-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

logs:
	docker-compose logs -f eig-cohesionneur

test:
	docker-compose run --rm eig-cohesionneur pytest

next-week:
	heroku run --type=web -a eig-cohesionneur python cli.py next-week

flush-db:
	heroku run --type=web -a eig-cohesionneur python cli.py flush-all