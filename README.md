# Smaug (Powerdrive Backend)
API source for the Powerdrive project

Powerdrive is a website that allows you to store and share files. It also provides a simple calendar allowing you to keep track of your events.

<a href="https://github.com/skni-umcs/powerdrive-front">Frontend</a> | <a href="https://powerdrive.skni.umcs.pl/">Website</a>

## Contributors 

<table>
  <tr>
    <td align="center"><a href="https://github.com/Buczkek"><img src="https://avatars.githubusercontent.com/u/42646328?v=4" width="110px;" alt=""/><br /><sub><b>Jakub Buczek</b></sub></a></td>
    <td align="center"><a href="https://github.com/jasieqb"><img src="https://avatars.githubusercontent.com/u/37178939?v=4" width="110px;" alt=""/><br /><sub><b>Jan Bylina</b></sub></a></td>
    <td align="center"><a href="https://github.com/kingastec"><img src="https://avatars.githubusercontent.com/u/78658172?v=4" width="110px;" alt=""/><br /><sub><b>Kinga Stec</b></sub></a></td>
    <td align="center"><a href="https://github.com/michalatra"><img src="https://avatars.githubusercontent.com/u/79483588?v=4" width="110px;" alt=""/><br /><sub><b>Michał Latra</b></sub></a></td>
    <td align="center"><a href="https://github.com/ciniss"><img src="https://avatars.githubusercontent.com/u/73825209?v=4" width="110px;" alt=""/><br /><sub><b>Bartosz Dąbrowski</b></sub></a></td>
  </tr>
</table>

[//]: # (## Installation)

## Requirements

docker \
docker-compose

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
