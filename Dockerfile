# syntax=docker/dockerfile:1.7

# ---------------------------------------------------------------------------
# Builder stage: resolve and install dependencies in an isolated environment
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Bring uv from the official image
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /usr/local/bin/

# Install build tools required to compile native wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency manifests to leverage Docker layer caching
COPY pyproject.toml uv.lock README.md LICENSE ./

# Install production dependencies into an isolated venv (no project yet)
RUN uv sync --frozen --no-dev --no-install-project

# Copy the source tree and install the project itself
COPY src ./src
RUN uv sync --frozen --no-dev

# ---------------------------------------------------------------------------
# Runtime stage: minimal image with a non-root user
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Create an unprivileged system user
RUN groupadd --system app \
    && useradd --system --gid app --home /app --shell /usr/sbin/nologin app

WORKDIR /app

# Copy only what is needed to run the application
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD ["python", "-m", "lab_cloud"]