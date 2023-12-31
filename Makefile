PROJECT_NAME := "smaug"
MAIN_CONTAINER := "smaug"
DB_CONTAINER := "db"
SERVER_CONTAINER := $(PROJECT_NAME)-$(MAIN_CONTAINER)

all: clear build up
	lazydocker

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

clear: drop_db
	docker compose down --rmi local --volumes --remove-orphans
	sudo rm -rf files
	sudo rm -rf smaug_media


clear_all:
	docker compose down --rmi all --volumes --remove-orphans

drop_db:
	docker compose down

	sudo rm -rf ./db_data

# make new_migration name="migration name"
new_migration:
	docker compose run --rm $(MAIN_CONTAINER) alembic revision --autogenerate -m "$(name)"

migration:
	docker compose run --rm $(MAIN_CONTAINER) alembic upgrade head
