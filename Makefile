COMPOSE_APP := docker-compose.yml
## up                  | Build and run the application
up:
	docker-compose -f ${COMPOSE_APP} build
	docker-compose -f ${COMPOSE_APP} up -d


## down                | Stop the application
down:
	docker-compose -f ${COMPOSE_APP} down --remove-orphans
