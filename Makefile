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

bash:
	docker-compose run --rm eig-cohesionneur bash

dev-new-week:
	docker-compose run --rm eig-cohesionneur python cli.py new-week -s 2020-01-01

dev-next-week:
	docker-compose run --rm eig-cohesionneur python cli.py next-week

dev-flush-db:
	docker-compose run --rm eig-cohesionneur python cli.py flush-all

prod-next-week:
	heroku run --type=web -a eig-cohesionneur python cli.py next-week

prod-flush-db:
	heroku run --type=web -a eig-cohesionneur python cli.py flush-all