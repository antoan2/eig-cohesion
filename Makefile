build:
	docker-compose build

up-dev:
	docker-compose up -d

up-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

logs:
	docker-compose logs -f eig-cohesion 

