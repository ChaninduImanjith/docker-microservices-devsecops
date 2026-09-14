# Enterprise Multi-Container Microservices Architecture (DevSecOps Enabled)

![Docker CI/CD DevSecOps Pipeline](https://github.com/ChaninduImanjith/docker-microservices-devsecops/actions/workflows/docker-ci.yml/badge.svg)

A production-grade, containerized microservices project demonstrating DevSecOps best practices, container security hardening, automated CI/CD security scanning, and multi-container orchestration using **FastAPI**, **Nginx**, **PostgreSQL**, and **Redis**.

---

## 🏗️ System Architecture

```text
[ Client Request ]
       │
       ▼
┌──────────────┐
│ Nginx Proxy  │
│   Port 80    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Backend API  │
│   FastAPI    │
└──────┬───────┘
       │
  ┌────┴───────────┐
  ▼                ▼
┌───────────┐   ┌───────────┐
│ PostgreSQL│   │   Redis   │
│ Database  │   │   Cache   │
└───────────┘   └───────────┘
```

The backend service is built using a **multi-stage Docker build** with an isolated Python virtual environment located at `/opt/venv`. The application runs as a non-root system user named `appuser`.

---

## 🔒 Security & DevSecOps Best Practices

- **Multi-Stage Docker Builds:** Reduces the final production image size by separating dependency installation and runtime stages.
- **Python Virtual Environment:** Python dependencies are installed inside an isolated virtual environment at `/opt/venv`, which is copied from the builder stage into the production image.
- **Non-Root Container Hardening:** The FastAPI application runs under an unprivileged system user (`appuser`) instead of `root`, reducing the impact of potential container compromise.
- **Minimal Base Images:** Lightweight `python:3.11-slim`, Alpine-based PostgreSQL, Redis, and Nginx images help reduce unnecessary packages and attack surface.
- **Dockerfile Static Analysis:** Automated Dockerfile linting using **Hadolint** helps enforce Docker security and maintainability best practices.
- **Automated Vulnerability Scanning:** **Trivy** scans the production container image in the CI/CD pipeline for `CRITICAL` and `HIGH` severity OS and dependency vulnerabilities.
- **GitHub Actions CI/CD:** Automated pipelines build, validate, scan, and publish container images whenever changes are pushed to the repository.
- **GitHub Container Registry (GHCR):** Production container images are automatically published to GHCR and tagged using both `latest` and the Git commit SHA.
- **Service Health Checks:** Application and infrastructure health endpoints allow container availability and dependency connectivity to be verified.
- **Service Isolation:** Docker Compose provides isolated container networking while exposing only the Nginx reverse proxy to client traffic.

---

## 🐍 Python Virtual Environment Architecture

The backend Docker image uses a dedicated Python virtual environment:

```text
Builder Stage
     │
     ├── Create /opt/venv
     │
     ├── Upgrade pip
     │
     └── Install requirements.txt
             │
             ▼
Production Stage
     │
     ├── Copy /opt/venv from builder
     ├── Add /opt/venv/bin to PATH
     ├── Copy application source code
     ├── Switch to non-root appuser
     └── Start FastAPI/Uvicorn
```

This approach keeps dependency installation isolated from the system Python environment and allows the runtime stage to reuse only the required Python packages.

Example environment configuration:

```dockerfile
ENV PATH="/opt/venv/bin:$PATH"
```

---

## 🚀 Quick Start (Local Deployment)

### Prerequisites

- Docker Engine v24+
- Docker Compose v2+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ChaninduImanjith/docker-microservices-devsecops.git
cd docker-microservices-devsecops
```

### 2. Build and Launch Services

```bash
docker compose up -d --build
```

### 3. Verify Container Status

```bash
docker compose ps
```

### 4. Test Endpoints via Nginx Proxy

```bash
curl http://localhost/
curl http://localhost/health
curl http://localhost/db-check
curl http://localhost/cache-check
```

| Endpoint | Purpose |
|---|---|
| `/` | Root API endpoint |
| `/health` | Backend application health check |
| `/db-check` | PostgreSQL connectivity check |
| `/cache-check` | Redis connectivity check |

### 5. View Container Logs

```bash
docker compose logs -f
```

### 6. Stop the Stack

```bash
docker compose down
```

To remove persistent volumes as well:

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` removes Docker volumes, including persistent PostgreSQL data.

---

## 🛠️ Tech Stack & Tooling

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| Runtime | Python 3.11 |
| Application Server | Uvicorn |
| Reverse Proxy | Nginx 1.25 Alpine |
| Database | PostgreSQL 15 Alpine |
| Cache | Redis 7 Alpine |
| Containerization | Docker |
| Orchestration | Docker Compose |
| CI/CD | GitHub Actions |
| Dockerfile Linting | Hadolint |
| Vulnerability Scanning | Trivy |
| Container Registry | GitHub Container Registry (GHCR) |

---

## 🔄 CI/CD DevSecOps Pipeline

```text
Developer Push
      │
      ▼
┌────────────────────┐
│   GitHub Actions   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Hadolint Analysis  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Docker Image Build │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Trivy CVE Scan     │
│ HIGH / CRITICAL    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Publish to GHCR    │
│ latest + commit SHA│
└────────────────────┘
```

The pipeline follows a **shift-left security approach**, where security checks are integrated directly into the software delivery lifecycle instead of being performed only after deployment.

---

## 📦 Container Services

```text
nginx
  └── backend
        ├── postgres
        └── redis
```

- **Nginx** handles incoming HTTP traffic and reverse proxies requests to the backend.
- **Backend** provides REST API endpoints using FastAPI.
- **PostgreSQL** provides persistent relational data storage.
- **Redis** provides fast in-memory caching.

---

## 🛡️ Security Design Summary

```text
Source Code
    │
    ▼
Dockerfile Linting
    │
    ▼
Multi-Stage Build
    │
    ▼
Python Virtual Environment
    │
    ▼
Minimal Runtime Image
    │
    ▼
Non-Root User
    │
    ▼
Trivy Vulnerability Scan
    │
    ▼
Secure Registry Publishing
    │
    ▼
Containerized Deployment
```

This architecture demonstrates how modern containerized applications can combine **microservices architecture**, **automation**, and **DevSecOps security practices** in a maintainable deployment workflow.
