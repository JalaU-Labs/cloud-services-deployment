.PHONY: install test lint format run clean docker-build docker-up docker-down

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

run:
	uv run python -m lab_cloud

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info

docker-build:
	docker build -t lab-cloud:latest .

docker-rebuild:
	docker compose build --no-cache

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f app