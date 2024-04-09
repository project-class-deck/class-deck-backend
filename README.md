# class-deck-backend

## Installation

### Poetry

For Mac OS

- install poetry

```sh
brew install poetry
```

- use python 3.12

```sh
poetry env use 3.12
```

- install packages

```sh
poetry install
```

if you don't want to use poetry just install from requirements

- how to add new dependencies and update requirements.txt

```sh
poetry add package_name
poetry export -f requirements.txt --output requirements.txt
```

### Postgresql

For Mac OS

- install posgresql

```sh
brew install postgresql@16
```

- run postgresql

```sh
brew services start postgresql@16
```

- create database

```sh
psql -U postgres
```

```sh
CREATE USER cardist WITH PASSWORD 'ineedmoretime1!';
CREATE DATABASE card_deck;
GRANT ALL PRIVILEGES ON DATABASE card_deck TO cardist;
ALTER DATABASE card_deck OWNER TO cardist;
```

- migrate

```sh
python manage.py migrate
```

- create superuser

```sh
python manage.py createsuperuser
```
