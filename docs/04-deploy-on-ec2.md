# Deploying the API on AWS EC2

This document explains how to deploy the FastAPI application on the EC2
instance, connect it to MongoDB Atlas, and expose it securely so that it can be
consumed from a local client.

## 1. Prerequisites

Before starting:

- The EC2 instance is running with a dedicated Security Group as described in
  `02-aws-ec2-setup.md`.
- Docker and Docker Compose are installed on the instance as described in
  `01-docker-installation.md`.
- The MongoDB Atlas cluster is active, the database user exists, and the
  **public IP of the EC2 instance** is in the Atlas Network Access whitelist
  (see `03-mongodb-atlas-setup.md`).

Verify the public IP of the instance:

```bash
curl ifconfig.me
```

If the returned IP is not in Atlas Network Access, add it before proceeding.

## 2. Cloning the Repository

On the EC2 instance:

```bash
sudo dnf install -y git
git clone git@gitlab.com:jala-university1/cohort-5/ES.CO.CSNT-245.GA.T2.26.M2/SD/week-07/alejandro-botina.git
cd alejandro-botina
```

If the repository is private, configure an SSH deploy key with read-only access
on the instance instead of copying a personal key. Alternatively, clone via
HTTPS with a personal access token that has only `read_repository` scope.

## 3. Creating the `.env` File

The application reads its configuration from environment variables. On the
instance, create the `.env` file:

```bash
cp .env.example .env
vi .env
```

Set at minimum:

```
MONGODB_URI=mongodb+srv://lab_reader_writer:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=lab_cloud
APP_ENV=production
```

Protect the file:

```bash
chmod 600 .env
```

Confirm that `.env` is listed in `.gitignore`:

```bash
grep '^\.env$' .gitignore
```

It must appear. If it does not, add it before committing anything else.

## 4. Building the Docker Image

The `docker-compose.yml` in the repository starts both MongoDB and the
application. On the EC2 instance, **only the application is needed**, since the
database is managed by Atlas. The local MongoDB service exists to simulate the
cloud environment during development.

Two options are available:

### Option A: Use Docker Compose with a profile (recommended)

Add a profile to the `mongo` service in `docker-compose.yml` so it is not
started unless explicitly requested:

```yaml
services:
  mongo:
    profiles: ["local"]
    # ... rest of the configuration

  app:
    # ... app configuration
```

Then, on the EC2 instance, run only the `app` service:

```bash
docker compose up -d app
```

The `app` service will use the `MONGODB_URI` from the `.env` file. On the
instance that URI points to Atlas.

### Option B: Build and run the container manually

```bash
docker build -t lab-cloud-api:latest .
docker run -d \
    --name lab-cloud-api \
    --restart unless-stopped \
    -p 8000:8000 \
    --env-file .env \
    lab-cloud-api:latest
```

This approach bypasses Compose entirely. It is simpler but less reproducible.

## 5. Verifying the Deployment

From the EC2 instance itself:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/contacts
```

From your local machine (with your public IP authorized in the Security Group):

```bash
curl http://<ec2-public-ip>:8000/
curl http://<ec2-public-ip>:8000/contacts
```

Test the creation endpoint:

```bash
curl -X POST http://<ec2-public-ip>:8000/contacts \
    -H "Content-Type: application/json" \
    -d '{"name": "Diego", "email": "diego@example.com"}'
```

Then list again:

```bash
curl http://<ec2-public-ip>:8000/contacts
```

The new contact should appear. This confirms that the EC2 instance is talking
to MongoDB Atlas.

## 6. Managing the Service

The container is configured with `restart: unless-stopped`, so it starts again
if the instance reboots.

To inspect logs:

```bash
docker compose logs -f app
# or, if using Option B:
docker logs -f lab-cloud-api
```

To stop:

```bash
docker compose down
# or
docker stop lab-cloud-api && docker rm lab-cloud-api
```

To update the application after a new commit:

```bash
git pull
docker compose up -d --build app
```

## 7. Exposing the API Safely

The Security Group controls which IPs can reach port 8000. The recommended
configuration for the lab is:

- Inbound SSH (22) from `<your-ip>/32`.
- Inbound TCP 8000 from `<your-ip>/32`.

If the API must be exposed to other users, the correct approach is to place it
behind a reverse proxy with TLS (Nginx or Caddy), obtain a certificate from
Let's Encrypt, and restrict access further with authentication. This lab does
not require that level of exposure.

**Do not open port 8000 to `0.0.0.0/0`.** Do not open port 27017 (MongoDB) at
all; the connection to Atlas goes outbound only.

## 8. Updating the Whitelist

When the EC2 instance is stopped and started again, its public IP may change
(unless an Elastic IP is attached). If the IP changes:

1. Retrieve the new IP on the instance: `curl ifconfig.me`.
2. Update the Atlas Network Access whitelist, removing the old entry.
3. Update the Security Group if you had restricted it to the old IP of your
   local machine.

To avoid this manual step, attach an Elastic IP to the instance. Note that
unattached Elastic IPs incur charges, so it must remain attached.

## 9. Screenshots to Capture

- `ec2-docker-ps.png` - `docker compose ps` showing the running container.
- `ec2-api-localhost.png` - `curl http://127.0.0.1:8000/` from the instance.
- `local-api-public.png` - `curl http://<public-ip>:8000/` from the local
  machine.
- `local-post-contact.png` - The POST request creating a contact.
- `atlas-data-view.png` - MongoDB Compass or Atlas UI showing the stored
  contact.