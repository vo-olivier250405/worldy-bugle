# Worldy Bugle

A geopolitical news map. Click a country on the interactive hexagonal world map to browse its latest press articles, collected automatically from international RSS feeds.

## Architecture

```
worldy-bugle/
├── worldy_bugle_api/   # Django REST API (Python 3.11)
└── client/             # React + TypeScript + Vite (Node 22)
```

The backend exposes a REST API consumed by the client. Article collection runs automatically via Celery workers pulling RSS feeds every hour.

## Prerequisites

### With Docker

- Docker >= 24
- Docker Compose >= 2

### Without Docker

- Python 3.11
- Node.js 22
- PostgreSQL
- Redis

---

## Getting started with Docker

**1. Configure environment variables**

Copy the example file and fill in the values:

```bash
cp worldy_bugle_api/.env.example worldy_bugle_api/.env
```

Required variables:

```
DJANGO_SECRET_KEY=<a long random string>
DJANGO_DEBUG=True

POSTGRES_DB=worldy_bugle
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

**2. Build and start all services**

```bash
docker compose up --build
```

This starts six containers: `api`, `celery`, `celery-beat`, `postgres`, `redis`, and `client`.

| Service    | URL                       |
| ---------- | ------------------------- |
| Client     | http://localhost:5175     |
| API        | http://localhost:8005/api |

**3. Apply migrations and load initial data**

In a second terminal, once the containers are running:

```bash
make migrate
make load_sources
```

**Rebuilding after dependency changes**

If you add packages to `requirements.txt` or `package.json`, rebuild to avoid stale layers:

```bash
docker compose down -v
docker compose up --build
```

The `-v` flag removes anonymous volumes so `node_modules` is reinstalled from scratch.

---

## Getting started without Docker

### Backend

**1. Create and activate a virtual environment**

```bash
cd worldy_bugle_api
python3.11 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_trf
```

**3. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and set `DB_HOST=localhost` (instead of the Docker service name `postgres`).

**4. Start PostgreSQL and Redis**

Make sure PostgreSQL and Redis are running locally on their default ports (5432 and 6379).

**5. Apply migrations and load initial data**

```bash
python manage.py migrate
python manage.py loaddata fixtures/sources.json
```

**6. Start the API server**

```bash
python manage.py runserver 0.0.0.0:8005
```

**7. Start Celery workers (optional — required for automatic article collection)**

In separate terminals:

```bash
celery -A config worker -l info
celery -A config beat -l info
```

### Client

```bash
cd client
npm install
npm run dev
```

The client starts at http://localhost:5175.

---

## Makefile commands

These commands require the Docker containers to be running.

| Command                               | Description                             |
| ------------------------------------- | --------------------------------------- |
| `make migrate`                        | Apply pending database migrations       |
| `make makemigrations`                 | Generate migrations from model changes  |
| `make load_sources`                   | Load RSS source fixtures                |
| `make shell`                          | Open a Django shell in the API container|
| `make backup_db`                      | Dump the database to `./backups/`       |
| `make clean_load_db DUMP_FILE=<path>` | Drop the database and restore from dump |
