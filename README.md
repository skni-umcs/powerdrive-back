# Smaug 
Api for the Powerdrive project

## Installation

## Requirements

## Development
To start the development server, run the following command:
```bash
docker compose up -d
```

This will start the development server on port 8000, and the database on port 5432.

## Tests:

To run all tests:

```bash
docker compose run --rm smaug test
```

## Migration:

To add new migrations:
import your SqlAlchemy model to [alembic/env.py](alembic/env.py) and run the following command:

```bash
make migration name=<migration_name>
```

Migrations are run automatically when starting the development container.
To run migrations manually:

```bash
make migrate
```
