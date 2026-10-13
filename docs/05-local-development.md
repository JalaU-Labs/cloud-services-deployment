# Local Development

This document explains how to work on the project locally, run tests, and use
the Docker Compose simulation of a cloud environment.

## 1. Requirements

- Python 3.14.6 or higher.
- `uv` 0.12.23 or higher.
- Docker Engine and Docker Compose.
- Git.
- An `.env` file created from `.env.example`.

## 2. First Setup

```bash
git clone git@gitlab.com:jala-university1/cohort-5/ES.CO.CSNT-245.GA.T2.26.M2/SD/week-07/alejandro-botina.git
cd alejandro-botina
make install
cp .env.example .env
```

Edit `.env` and set `MONGODB_URI` to either the local Docker URI or the Atlas
URI, depending on what you want to test.

## 3. Common Make Targets

The `Makefile` provides the following targets:

| Target         | Description                                                |
|----------------|------------------------------------------------------------|
| `install`      | Install dependencies with `uv sync --extra dev`.           |
| `test`         | Run `pytest` with coverage.                                |
| `lint`         | Run `ruff check`.                                          |
| `format`       | Run `ruff format`.                                         |
| `run`          | Run the FastAPI app with uvicorn on port 8000.             |
| `clean`        | Remove caches and build artifacts.                         |
| `docker-build` | Build the Docker image manually.                           |
| `docker-rebuild` | Rebuild the Compose image ignoring the cache.            |
| `docker-up`    | Start the Compose environment (forces rebuild of `app`).   |
| `docker-down`  | Stop and remove the Compose environment.                   |
| `docker-logs`  | Follow the logs of the `app` container.                    |

## 4. Running the Tests

```bash
make test
```

The test suite uses `mongomock` for the database layer, so no real MongoDB
connection is needed. Coverage is reported to the terminal. Aim to keep total
coverage above 90%.

## 5. Running the Linter

```bash
make lint
```

`ruff` is configured with a modern rule set. If it complains about a trailing
newline (`W292`) or unsorted imports (`I001`), run:

```bash
uv run ruff check --fix
```

Then verify again with `make lint`.

## 6. Running the Application Locally

### Option A: Against the local MongoDB container

```bash
make docker-up
curl http://127.0.0.1:8000/
```

The Compose file binds `app` to the internal hostname `mongo:27017` regardless
of what `MONGODB_URI` says in the host `.env`. This is intentional: the
container should not reach out to Atlas during local simulations.

### Option B: Against MongoDB Atlas

```bash
make run
```

In this mode the application reads `MONGODB_URI` from the host `.env` and
connects directly to Atlas. Use this to validate the real cloud integration
from your local machine.

## 7. Directory Structure

```
src/lab_cloud/
├── __init__.py          Package version.
├── __main__.py          Entry point for `python -m lab_cloud`.
├── app.py               FastAPI application and routes registration.
├── config.py            Settings loaded from environment variables.
├── db.py                MongoDB client management.
├── schemas.py           Pydantic schemas.
└── routes/
    ├── __init__.py
    └── contacts.py      /contacts endpoints.
```

## 8. Adding a New Endpoint

1. Create or edit a module under `src/lab_cloud/routes/`.
2. Define the Pydantic schemas under `src/lab_cloud/schemas.py`.
3. Register the router in `src/lab_cloud/app.py` with
   `app.include_router(...)`.
4. Add a test under `tests/`.
5. Run `make lint` and `make test`.
6. Commit with a descriptive message.