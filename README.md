# FastAPI Boilerplate

## Setup

### Clone your repo

- Clone your repository after creating it with this template.

### Start up the FastAPI server

- Install Poetry:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

- Install project dependencies using Poetry:

```sh
poetry install
```

- Activate the virtual environment managed by Poetry:

```sh
poetry shell
```

- Create a `.env` file by copying the `.env.sample` file:

```sh
cp .env.sample .env
```

- Start the server:

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Setup database

To set up the database, follow the following steps:

- **Create your local database**

```bash
sudo -u <user> psql
```

```sql
CREATE DATABASE database_name;
```

- **Making migrations**

```bash
alembic revision --autogenerate -m 'initial migration'
alembic upgrade head
```

- **Adding tables and columns to models**
  After creating new tables or adding new models, make sure to run:

```bash
alembic revision --autogenerate -m "Migration message"
```

After creating new tables or adding new models, make sure you import the new model properly in the `app/api/models/__init__.py` file.

After importing it in the `__init__.py` file, you don't need to import it in the `/alembic/env.py` file anymore.
