# Cloud Services Deployment Lab

Week 7 laboratory project for the course "Redes de Computadoras 2" at Jala University.

This repository documents the practical exploration of cloud computing services, the
deployment of secure free-tier instances, and the local simulation of cloud
environments using Docker. It covers the three main service models (IaaS, PaaS, SaaS)
and applies security best practices for remote access and credential management.

## Table of Contents

1. [Project Description](#project-description)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Documentation](#documentation)
5. [Project Structure](#project-structure)
6. [Local Cloud Simulation with Docker](#local-cloud-simulation-with-docker)
7. [Activity 1 - Cloud Services on AWS Educate](#activity-1---cloud-services-on-aws-educate)
8. [Activity 2 - MongoDB Atlas Free Tier Cluster](#activity-2---mongodb-atlas-free-tier-cluster)
9. [Reflection: Cloud vs. Local Docker](#reflection-cloud-vs-local-docker)
10. [Theoretical Questions](#theoretical-questions)
11. [Security Best Practices](#security-best-practices)
12. [Cost Safety on AWS](#cost-safety-on-aws)
13. [CI/CD Pipelines](#cicd-pipelines)
14. [Testing](#testing)
15. [License](#license)
16. [Author](#author)

---

## Project Description

The laboratory is divided into two complementary activities:

- **Activity 1:** Creation and analysis of cloud services on a free-tier educational
  provider (AWS Educate), classification of services by model (IaaS, PaaS, SaaS),
  deployment of a small virtual server, and secure remote access.
- **Activity 2:** Deployment of a free MongoDB Atlas cluster, configuration of
  Network Access and Database Access with strict security, connection from a local
  client, and integration with a Python application through environment variables.

Docker is used to simulate a local cloud environment that mirrors the remote
deployment, allowing comparison between on-premise containers and managed cloud
services.

---

## Prerequisites

- Python 3.14.6 or higher
- [uv](https://github.com/astral-sh/uv) 0.12.23 or higher
- Docker Engine 29.x and Docker Compose 5.x
- Git
- An AWS Educate account (free)
- A MongoDB Atlas account (free tier)
- A local MongoDB client such as [MongoDB Compass](https://www.mongodb.com/products/compass)

---

## Quick Start

```bash
# Clone the repository
git clone git@gitlab.com:jala-university1/cohort-5/ES.CO.CSNT-245.GA.T2.26.M2/SD/week-07/alejandro-botina.git
cd cloud-services-deployment

# Install dependencies
make install

# Copy the environment variables template
cp .env.example .env

# Edit .env with your real MongoDB Atlas credentials before running

# Run linting and tests
make lint
make test

# Build and start the local Docker environment
make docker-build
make docker-up

# Verify the application
curl http://127.0.0.1:8000/

# Stop the local environment
make docker-down
```

---

## Documentation

Detailed guides are available under `docs/`:

| Document | Purpose |
|---|---|
| [01 - Docker Installation](docs/01-docker-installation.md) | Install Docker Engine and Compose on Arch, Ubuntu, and Amazon Linux. |
| [02 - AWS EC2 Setup](docs/02-aws-ec2-setup.md) | Create the EC2 instance and configure Security Groups safely. |
| [03 - MongoDB Atlas Setup](docs/03-mongodb-atlas-setup.md) | Create the free cluster, configure Network and Database Access. |
| [04 - Deploy on EC2](docs/04-deploy-on-ec2.md) | Deploy the API on EC2 connected to MongoDB Atlas. |
| [05 - Local Development](docs/05-local-development.md) | Work on the project locally, run tests, use Docker Compose. |
| [06 - Security Hardening](docs/06-security-hardening.md) | Consolidated security practices and incident response. |
| [07 - Troubleshooting](docs/07-troubleshooting.md) | Common errors and their fixes. |

---

## Project Structure

```
.
├── docs/
│   ├── screenshots/
│   ├── 01-docker-installation.md
│   ├── 02-aws-ec2-setup.md
│   ├── 03-mongodb-atlas-setup.md
│   ├── 04-deploy-on-ec2.md
│   ├── 05-local-development.md
│   ├── 06-security-hardening.md
│   └── 07-troubleshooting.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitlab-ci.yml
├── src/
│   └── lab_cloud/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── config.py
│       ├── db.py
│       ├── schemas.py
│       └── routes/
│           ├── __init__.py
│           └── contacts.py
├── tests/
│   ├── test_app.py
│   ├── test_db.py
│   └── test_placeholder.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
├── docker-compose.yml
└── uv.lock
```

---

## Local Cloud Simulation with Docker

The `docker-compose.yml` file defines two services that simulate a cloud
environment locally:

- **mongo:** a MongoDB 7.0 container with authentication enabled and data
  persisted in a named volume.
- **app:** the FastAPI application built from the multi-stage `Dockerfile`,
  running as a non-root user, connected to the local MongoDB instance.

Both services expose their ports only on `127.0.0.1`, never on `0.0.0.0`, to
prevent unintended network exposure.

Note that the `app` container is configured to reach the local `mongo`
container through its internal hostname (`mongo:27017`). The `MONGODB_URI`
variable defined in the host `.env` file is intentionally **not** forwarded
to the container, because it points to MongoDB Atlas and would bypass the
local simulation. To test the application against MongoDB Atlas, run it
outside Docker with `make run`, which loads the `.env` file directly.

Run the environment:

```bash
make docker-up
```

Check the container status:

```bash
docker compose ps
```

Expected output: both services in `running` state, `mongo` marked as `healthy`.

Stop and remove the containers:

```bash
make docker-down
```

---

## Activity 1 - Cloud Services on AWS Educate

### Step 1 - Account creation

1. Navigate to [AWS Educate](https://aws.amazon.com/education/awseducate/).
2. Register with your institutional email address.
3. Complete the student verification process.
4. Once approved, sign in to the AWS Educate portal and open the AWS Console
   through the "AWS Educate Starter Account" or the classroom assigned by the
   institution.
5. Record the account identifier provided by AWS. For this lab the account
   reference is `arn:aws:account::303971476941:account`.

Document each step with a screenshot in the `docs/screenshots/` folder
(create it if it does not exist) and reference the file names in this section.

### Step 2 - Service exploration and classification

Three services available in the free tier are analyzed below.

| Service              | Model | Functionality                                                                 | Typical industrial use                                              |
|----------------------|-------|-------------------------------------------------------------------------------|---------------------------------------------------------------------|
| Amazon EC2           | IaaS  | Provides resizable virtual machines with full control over the OS and network.| Hosting custom applications, batch processing, legacy migrations.  |
| AWS Elastic Beanstalk| PaaS  | Deploys applications automatically handling scaling and load balancing.        | Web application deployment without infrastructure management.      |
| Amazon S3            | SaaS  | Object storage service accessible through an API or web console.              | Backups, static site hosting, media storage.                        |

Alternative classifications accepted: Amazon RDS as PaaS, AWS Lambda as FaaS
(a subset of PaaS), Google Workspace as SaaS.

### Step 3 - Deployment of a practical instance

1. In the AWS Console, open the EC2 dashboard.
2. Select "Launch instance".
3. Choose an Amazon Linux 2023 AMI (free tier eligible).
4. Choose the `t2.micro` or `t3.micro` instance type (free tier eligible).
5. Create a new key pair in `.pem` format and store it locally with restricted
   permissions:

   ```bash
   chmod 400 ~/.ssh/lab-cloud-key.pem
   ```

6. In the network settings, create a security group with the following rules:

   - Inbound SSH (port 22) restricted to the current public IP address only.
   - No inbound rules open to `0.0.0.0/0` except HTTP/HTTPS if strictly required
     for testing.

7. Launch the instance and wait until its state is `running`.

8. Connect from the local machine:

   ```bash
   ssh -i ~/.ssh/lab-cloud-key.pem ec2-user@<public-ip>
   ```

9. Validate connectivity by running `hostname` and `uname -a` on the remote
   host.

Capture screenshots of the account creation, the service list, the instance
configuration, and the SSH session.

### Step 4 - Comparison between IaaS, PaaS, and SaaS

| Aspect                  | IaaS                                       | PaaS                                            | SaaS                                     |
|-------------------------|--------------------------------------------|-------------------------------------------------|------------------------------------------|
| What the provider gives | Virtual hardware, storage, and networking  | Runtime, middleware, and deployment tooling     | A complete application                   |
| What the user manages   | OS, runtime, applications, and data        | Applications and data only                      | Only data and user access                |
| Level of control        | High                                       | Medium                                          | Low                                      |
| Example                 | Amazon EC2                                 | AWS Elastic Beanstalk, MongoDB Atlas            | Amazon S3, Google Workspace              |
| Comparison with local   | Equivalent to a physical or virtual server | Equivalent to a preconfigured Docker host       | Equivalent to a hosted web application   |

The local Docker environment of this repository behaves like a simplified IaaS:
the developer controls the OS image, the network, and the runtime, but the host
machine itself remains under full local control.

---

## Activity 2 - MongoDB Atlas Free Tier Cluster

### Step 1 - Account and cluster creation

1. Navigate to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register).
2. Register with a personal or institutional email address.
3. Create an organization and a project.
4. Select "Build a Database" and choose the **M0 Free Tier** cluster.
5. Choose a cloud provider and region close to the user location to reduce
   latency.
6. Name the cluster, for example `lab-cloud-cluster`, and confirm the creation.

### Step 2 - Network Access configuration

1. Open the "Network Access" section in the left sidebar.
2. Click "Add IP Address".
3. Add the current public IP address only. To find it:

   ```bash
   curl ifconfig.me
   ```

4. Do **not** add `0.0.0.0/0` (Allow Access from Anywhere). This option exposes
   the database to the entire Internet and is one of the most common causes of
   data leaks in MongoDB Atlas.
5. If the IP changes frequently, use a temporary entry with a short expiration
   instead of a wide-open range.

### Step 3 - Database Access configuration

1. Open the "Database Access" section.
2. Click "Add New Database User".
3. Select "Password" as the authentication method.
4. Choose a username that does not reveal the purpose of the cluster, for
   example `lab_reader_writer`.
5. Generate a strong password using a password manager. Do not reuse
   credentials from other services.
6. Assign the "Read and write to any database" role for this lab. In production,
   scope the role to the specific database.
7. Save the user.

### Step 4 - Connection string

1. Open the cluster overview and click "Connect".
2. Select "Drivers" and then "Python" with the driver version 4.x or higher.
3. Copy the connection string. It has the following form:

   ```
   mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```

4. Replace `<username>` and `<password>` with the values created in Step 3.
5. Store the resulting string in the local `.env` file (which is git-ignored):

   ```
   MONGODB_URI=mongodb+srv://lab_reader_writer:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB=lab_cloud
   ```

### Step 5 - Local connection validation

1. Install MongoDB Compass or a similar client.
2. Paste the connection string from the `.env` file.
3. Connect and confirm that the cluster is reachable.
4. Optionally create a database named `lab_cloud` and a collection named
   `contacts`.
5. Verify the connection from Python:

   ```bash
   uv run python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.environ['MONGODB_URI']); print(client.admin.command('ping'))"
   ```

   Expected output: `{'ok': 1.0}`.

Capture screenshots of the cluster creation, the Network Access configuration
with a single IP, the Database Access user, and the successful connection.

---

## Reflection: Cloud vs. Local Docker

The two approaches complement each other rather than compete.

### Advantages of using cloud services

- **Elasticity:** resources scale on demand without hardware procurement.
- **Managed operations:** backups, monitoring, and patching are handled by the
  provider.
- **Global reach:** services can be deployed close to the end users.
- **Pay-as-you-go:** no upfront capital expenditure.

### Disadvantages of using cloud services

- **Recurring cost:** charges accumulate as usage grows, especially outside the
  free tier.
- **Vendor lock-in:** migrating away from a provider's managed services can be
  expensive.
- **Reduced control:** the OS and the runtime are configured by the provider.
- **Network dependency:** access requires a stable Internet connection.
- **Security surface:** misconfigured access rules are a common source of
  leaks.

### Advantages of local Docker simulation

- **Zero cost:** everything runs on the developer's machine.
- **Full control:** the OS, the runtime, and the network are configurable.
- **Offline work:** no Internet connection is required.
- **Fast iteration:** containers start in seconds.
- **Reproducibility:** the same `docker-compose.yml` runs identically on any
  host with Docker.

### Disadvantages of local Docker simulation

- **No real cloud behavior:** load balancing, autoscaling, and geographic
  redundancy are not exercised.
- **Local resource limits:** CPU, memory, and disk depend on the developer's
  machine.
- **Manual security:** firewalls, TLS, and secret rotation must be implemented
  by hand.
- **No SLA:** the local environment offers no availability guarantee.

The cloud is preferable for production workloads that require resilience and
scale. Docker is preferable for development, testing, and teaching, where cost
and iteration speed matter more than availability.

---

## Theoretical Questions

### In which category does MongoDB Atlas fit and why?

MongoDB Atlas fits the **PaaS (Platform as a Service)** model. The provider
manages the underlying infrastructure (servers, storage, network, replicas, and
backups) and also the database engine itself (version, patches, and
configuration). The user only manages the data, the schema, and the access
control. This is the defining characteristic of PaaS: the platform is delivered
as a managed service while the developer focuses on the application.

### What is the advantage of using MongoDB Atlas over a natively installed instance?

- **Managed operations:** automatic backups, monitoring, and patching.
- **Horizontal scalability:** the cluster can grow without reinstalling anything.
- **High availability:** replica sets are configured by default across
  availability zones.
- **Global distribution:** read replicas can be placed close to end users.
- **Security defaults:** encryption at rest and in transit is enabled by
  default.
- **Reduced operational cost:** no need to maintain servers, OS updates, or
  hardware.

### What is the risk of using `Allow Access from Anywhere (0.0.0.0/0)`?

Opening the cluster to `0.0.0.0/0` allows any host on the Internet to attempt a
connection. Combined with weak or leaked credentials, this enables brute-force
attacks, data exfiltration, and ransomware. MongoDB databases exposed in this
way have historically been the target of automated scraping tools. The
recommended practice is to whitelist only the specific IP addresses that need
access, or to use private endpoints (AWS PrivateLink or Azure Private Link) in
production.

### What are the risks of storing credentials directly in the source code?

- **Permanent leak:** once committed, credentials remain in the Git history even
  if they are removed in a later commit.
- **Wide exposure:** anyone with read access to the repository can retrieve them.
- **No rotation:** rotating a leaked credential requires code changes and
  redeployment.
- **Compliance violations:** storing secrets in code breaks most security
  standards (ISO 27001, SOC 2, PCI DSS).

The correct approach is to store secrets in environment variables loaded from a
`.env` file that is git-ignored, or in a secret manager (AWS Secrets Manager,
HashiCorp Vault, GitLab CI/CD variables).

---

## Security Best Practices

The following practices are enforced in this project:

1. `.env` files are git-ignored. Only `.env.example` is versioned.
2. MongoDB Atlas Network Access is restricted to the current public IP, never
   `0.0.0.0/0`.
3. Database users have strong passwords generated by a password manager.
4. The Docker container runs as a non-root user (`app`).
5. Container ports are bound to `127.0.0.1`, never to `0.0.0.0`.
6. SSH keys are stored with `chmod 400` permissions.
7. CI/CD pipelines never contain credentials in plain text; they use the
   secret stores of GitLab and GitHub.
8. The Dockerfile uses a multi-stage build to minimize the runtime image and
   reduce the attack surface.

---

## Cost Safety on AWS

The laboratory uses only free-tier eligible resources. To avoid unexpected
charges:

1. Use only `t2.micro` or `t3.micro` instance types.
2. Stop the EC2 instance when it is not in use. Stopping is free; only the
   attached EBS volume incurs a minimal cost after the free-tier period.
3. Terminate the instance at the end of the lab to release all resources.
4. Do not attach Elastic IPs unless strictly necessary. Unattached Elastic IPs
   incur charges.
5. Monitor the Billing Dashboard weekly.
6. Set a zero-dollar budget alert in AWS Budgets.
7. Avoid services outside the free tier such as NAT Gateways, RDS instances
   with multi-AZ, or large S3 storage.
8. Delete unused snapshots and volumes.

---

## CI/CD Pipelines

Two pipelines are configured:

- **GitLab CI** (`.gitlab-ci.yml`): runs `ruff` and `pytest` on every push.
- **GitHub Actions** (`.github/workflows/ci.yml`): runs the same checks on every
  push and pull request.

Both pipelines install `uv` 0.12.23, synchronize dependencies from `uv.lock`,
and execute the same commands available locally through the `Makefile`, ensuring
that the results are reproducible in any environment.

---

## Testing

Tests are written with `pytest` and include coverage reporting via
`pytest-cov`. To run them:

```bash
make test
```

The coverage report is printed to the terminal. Current coverage focuses on the
FastAPI application and the package metadata.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.

---

## Author

Diego Alejandro Botina
Software Engineering Student
Jala University