# Troubleshooting

This document collects the errors encountered during the lab and the steps to
resolve them.

## 1. `uv sync` fails with `Readme file does not exist`

Cause: `pyproject.toml` references `README.md` but the file is missing or not
committed.

Fix:

```bash
ls README.md
# If missing, create it and commit
git add README.md
git commit -m "docs: add initial README"
```

## 2. `uv.lock` is not tracked by Git

Cause: `.gitignore` contains `uv.lock`.

Fix: remove the line and re-add the file.

```bash
sed -i '/^uv\.lock$/d' .gitignore
git add .gitignore uv.lock
git commit -m "fix: stop ignoring uv.lock"
```

## 3. `make lint` fails with `W292 No newline at end of file`

Cause: one or more files do not end with a newline.

Fix:

```bash
uv run ruff check --fix
git add .
git commit -m "style: add missing trailing newlines"
```

## 4. `B008 Do not perform function call in argument defaults`

Cause: FastAPI dependencies declared as `db: Database[Any] = Depends(...)`.

Fix: use `Annotated`.

```python
from typing import Annotated
from fastapi import Depends

DatabaseDep = Annotated[Database[Any], Depends(get_database)]

def endpoint(db: DatabaseDep) -> ...:
    ...
```

## 5. `pymongo.errors.ServerSelectionTimeoutError: 127.0.0.1:27017 Connection refused`

Cause: the containerized application is trying to reach `127.0.0.1:27017`
inside its own network namespace instead of the `mongo` service hostname.

Fix: in `docker-compose.yml`, set the URI to the internal hostname:

```yaml
environment:
  MONGODB_URI: mongodb://admin:changeme@mongo:27017/?authSource=admin
```

Do not forward the host `MONGODB_URI` to the container.

## 6. `pymongo.errors.ServerSelectionTimeoutError` against Atlas

Causes and fixes:

- The public IP of the client is not in Network Access. Add it.
- The password contains characters that must be URL-encoded (`@`, `:`, `/`).
- The cluster is paused. Resume it from the Atlas UI.
- The DNS resolver is not working. Try `dig +short <cluster>.mongodb.net`.

## 7. `docker compose up` recreates the container but the code is stale

Cause: Compose reuses the cached image unless `--build` is passed.

Fix:

```bash
make docker-down
make docker-up   # uses --build internally
```

Or:

```bash
docker compose build --no-cache app
docker compose up -d
```

## 8. `uv: command not found` in CI

Cause: the `uv` installer places the binary in `$HOME/.local/bin`, but the CI
job's `PATH` does not include it.

Fix:

```yaml
before_script:
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - uv sync --extra dev
```

## 9. `Permission denied (publickey)` when connecting to EC2

Causes:

- Wrong key file.
- The key file has overly permissive permissions.
- The username is not `ec2-user` for Amazon Linux.
- The instance's Security Group does not allow your IP on port 22.

Fixes:

```bash
chmod 400 ~/.ssh/lab-cloud-key.pem
ssh -i ~/.ssh/lab-cloud-key.pem ec2-user@<public-ip> -v
```

The `-v` flag prints the authentication attempts and shows exactly which key
was offered.

## 10. `SSH connection times out` to EC2

Causes:

- The Security Group does not allow your current IP on port 22.
- The instance is stopped.
- The instance has no public IP.
- A corporate firewall blocks outbound SSH.

Fixes:

- Update the Security Group with the current IP.
- Verify the instance state in the console.
- Try from a mobile hotspot to rule out local network issues.

## 11. `502 Bad Gateway` on a reverse proxy

Cause: the upstream container is not listening on the expected port, or the
proxy points to the wrong hostname.

Fix:

```bash
docker compose logs app
docker compose ps
curl http://127.0.0.1:8000/
```

Verify that the application responds locally before troubleshooting the proxy.

## 12. `ModuleNotFoundError: No module named 'lab_cloud'`

Cause: the package was not installed in the active virtual environment, or
`pythonpath` is not set correctly in `pytest`.

Fix:

```bash
uv sync --extra dev
uv run python -c "import lab_cloud; print(lab_cloud.__version__)"
```

If the import works inside `uv run` but not in `pytest`, verify that
`pyproject.toml` has:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
```