# Cloud Services Deployment Lab

Week 7 laboratory project for the course "Redes de Computadoras 2" at Jala University.

## Description

This project demonstrates the deployment and configuration of cloud services using free-tier providers, focusing on IaaS, PaaS, and SaaS models. It includes practical work with AWS and MongoDB Atlas, secure credential management, and local simulation using Docker.

## Prerequisites

- Python 3.14.6 or higher
- uv 0.12.23 or higher
- Docker and Docker Compose (for local simulation)
- Git

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitlab-ci.yml
├── src/
│   └── lab_cloud/
│       └── __init__.py
├── tests/
│   └── test_placeholder.py
├── .env.example
├── .gitignore
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

## Setup

1. Clone the repository:
   ```bash
   git clone git@gitlab.com:jala-university1/cohort-5/ES.CO.CSNT-245.GA.T2.26.M2/SD/week-07/alejandro-botina.git
   cd cloud-services-deployment
   ```

2. Install dependencies:
   ```bash
   make install
   ```

3. Copy the environment variables template and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

## Usage

- Run linting:
  ```bash
  make lint
  ```

- Run tests:
  ```bash
  make test
  ```

- Format code:
  ```bash
  make format
  ```

- Run the application:
  ```bash
  make run
  ```

## CI/CD

The project includes pipelines for both GitLab CI (`.gitlab-ci.yml`) and GitHub Actions (`.github/workflows/ci.yml`). Both pipelines perform static analysis (ruff) and run tests (pytest) on every push to the `main` branch.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Diego Alejandro Botina