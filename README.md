# Flashcards API

A REST API for studying using flashcards. Create and organise your flashcards into collections (decks), with full user authentication and account management.

Built as a learning project to practise Python backend development.

## Tech stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Pydantic** — data validation
- **Alembic** — database migrations
- **Docker** — PostgreSQL container
- **pytest** — automated test suite
- **JWT** — authentication with access and refresh tokens
- **Argon2** — password hashing

## Running locally

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python package manager
- [Docker](https://www.docker.com/) — for the PostgreSQL container

### Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/flashcards.git
cd flashcards
```

2. Create a `.env` file in the root directory

```env
DB_USER=admin
DB_PASSWORD=admin
DB_NAME=flashcards
DB_PORT=5432

JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Start the PostgreSQL container

```bash
docker compose up -d
```

4. Run database migrations

```bash
uv run alembic upgrade head
```

5. Start the API

```bash
uv run main.py
```

The API will be running at `http://localhost:8000`.

Interactive docs available at `http://localhost:8000/docs`.

## API overview

### Auth — `/auth`
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Create an account |
| POST | `/auth/login` | Log in and receive tokens |
| POST | `/auth/logout` | Log out |
| POST | `/auth/refresh` | Refresh access token |

### User — `/user`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/user/profile` | Get current user profile |
| PATCH | `/user/update` | Update email, password or nickname |

### Decks — `/decks`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/decks/` | List all decks |
| POST | `/decks/` | Create a deck |
| GET | `/decks/{id}` | Get a deck |
| PATCH | `/decks/{id}` | Update a deck |
| DELETE | `/decks/{id}` | Delete a deck |

### Flashcards — `/decks/{deck_id}/flashcards`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | List all flashcards in a deck |
| POST | `/` | Create a flashcard |
| GET | `/{id}` | Get a flashcard |
| PATCH | `/{id}` | Update a flashcard |
| DELETE | `/{id}` | Delete a flashcard |

## Running tests

Start the test database container first (runs on port 5433):

```bash
docker compose up -d db_test
```

Then run the test suite:

```bash
uv run pytest -v
```
