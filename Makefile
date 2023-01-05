PROJECT_NAME := "smaug"
MAIN_CONTAINER := "smaug"
DB_CONTAINER := "db"
SERVER_CONTAINER := $(PROJECT_NAME)-$(MAIN_CONTAINER)

all: clear build up

#docker up:
up:
	docker compose up -d

#docker build:
build:
	docker compose build --no-cache

down stop:
	docker compose down

test:
	docker compose run --rm $(MAIN_CONTAINER) test

bash:
	docker compose exec $(MAIN_CONTAINER) bash

bash_db:
	docker compose exec $(DB_CONTAINER) bash

clear:
	docker compose down --rmi all --volumes --remove-orphans
	docker image rm $(SERVER_CONTAINER):latest

drop_db:
	docker compose down
	docker compose run --rm $(MAIN_CONTAINER) drop_db