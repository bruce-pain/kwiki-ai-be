# Kwiki AI Backend

A FastAPI backend for Kwiki AI, providing user authentication, flashcard deck generation using LLMs, and CRUD APIs for decks and flashcards.

---

## Features

- User registration, login, and Google OAuth2 authentication
- JWT-based authentication and token refresh
- Generate flashcard decks using LLMs (Groq API)
- CRUD operations for decks and flashcards
- Rate limiting and robust error handling
- Alembic-powered migrations for PostgreSQL
- Modular, production-ready FastAPI structure

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/bruce-pain/kwiki-ai-be
cd kwiki-ai-be
```

### 2. Install Poetry

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install Dependencies

```sh
poetry install
```

### 4. Configure Environment Variables

Copy the sample environment file and fill in your secrets:

```sh
cp .env.sample .env
```

Edit `.env` and set values for database, secret keys, and API credentials.

### 5. Activate the Virtual Environment

```sh
poetry shell
```

### 6. Set Up the Database

- **Create your local PostgreSQL database:**

```sh
sudo -u <user> psql
```

```sql
CREATE DATABASE <database_name>;
```

- **Run migrations:**

```sh
alembic upgrade head
```

---

## Running the Server

Start the FastAPI server:

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at [http://localhost:8000/v1/docs](http://localhost:8000/v1/docs)

---

## Development

- **Create new migrations after model changes:**

```sh
alembic revision --autogenerate -m "Describe your change"
alembic upgrade head
```

- **Import new models in [`app/api/models/__init__.py`](app/api/models/__init__.py) for Alembic to detect them.**

---

## Testing

Run tests with:

```sh
poetry run pytest
```

---

## Project Structure

```
app/
  api/           # API routes, models, services, repositories
  core/          # Core config, base classes, dependencies
  db/            # Database session and base
  utils/         # Utility modules (JWT, logging, etc.)
alembic/         # Database migrations
tests/           # Unit tests
```

---

## License

This project is licensed under the Apache 2.0 License. See [LICENSE](LICENSE) for details.
