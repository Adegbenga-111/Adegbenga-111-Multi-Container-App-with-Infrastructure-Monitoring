# Kubernetes Task Manager — Containerization & Infrastructure Monitoring

A multi-container Task Manager application built to demonstrate containerization, service orchestration, infrastructure monitoring, and the path from Docker Compose to Kubernetes.

The project combines a React frontend, a FastAPI backend, and MongoDB, with Mongo Express for database administration and a monitoring stack built around Prometheus, Grafana, cAdvisor, and a MongoDB exporter.

The goal is to build a practical infrastructure project that demonstrates how to deploy, connect, monitor, and troubleshoot a containerized application.

## Table of Contents

- [Introduction](#introduction)
- [Project Objectives](#project-objectives)
- [Technology Stack](#technology-stack)
- [Infrastructure Architecture](#infrastructure-architecture)
- [Services and Responsibilities](#services-and-responsibilities)
- [Application Features](#application-features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Accessing the Services](#accessing-the-services)
- [Monitoring and Observability](#monitoring-and-observability)
- [Errors Encountered and Fixes](#errors-encountered-and-fixes)
- [Quick Troubleshooting Reference](#quick-troubleshooting-reference)
- [Project Roadmap](#project-roadmap)
- [Learning Outcomes](#learning-outcomes)
- [Security Notes](#security-notes)

## Introduction

Modern applications are rarely deployed as a single process. They typically consist of multiple services that communicate over a network, store persistent data, and require continuous monitoring.

This project explores that architecture by deploying a Task Manager application using Docker Compose.

The application separates the user interface, API, and database into individual containers. Supporting services provide browser-based database administration and infrastructure metrics, allowing the application to be inspected and monitored during operation.

The initial deployment uses Docker Compose. The next stage is to migrate the application to Kubernetes and extend the project with container orchestration, health monitoring, and deployment automation.

## Project Objectives

- Containerize a React frontend and Python backend.
- Deploy MongoDB as a persistent database service.
- Orchestrate multiple containers using Docker Compose.
- Configure service-to-service communication and port mappings.
- Manage persistent data using Docker volumes.
- Inspect database records through Mongo Express.
- Collect container, application, and database metrics using cAdvisor, FastAPI instrumentation, a MongoDB exporter, and Prometheus.
- Visualize monitoring data using Grafana dashboards.
- Troubleshoot container startup, health checks, and connectivity.
- Progress toward a Kubernetes deployment with infrastructure monitoring.

## Technology Stack

| Technology | Purpose |
|---|---|
| React | Frontend user interface |
| Python | Backend programming language |
| FastAPI | REST API framework |
| prometheus-fastapi-instrumentator | Exposes FastAPI request metrics at `/metrics` |
| MongoDB | Document-oriented database |
| Mongo Express | Browser-based MongoDB administration |
| Percona MongoDB Exporter | Exposes MongoDB statistics as Prometheus metrics |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Nginx | Serves the compiled React frontend |
| cAdvisor | Collects container resource metrics |
| Prometheus | Scrapes and stores time-series metrics |
| Grafana | Monitoring dashboards and visualization |
| Kubernetes | Planned container orchestration stage |
| Git and GitHub | Version control and project documentation |

## Infrastructure Architecture

The following diagram represents the current Docker Compose design.

![Architecture Diagram]()


### Architecture Overview

1. **Frontend:** Nginx serves the compiled React application to the browser.
2. **Backend:** FastAPI exposes REST endpoints for creating, retrieving, updating, and deleting tasks, plus a `/metrics` endpoint for Prometheus.
3. **Database:** MongoDB stores task records and persists them using a Docker volume.
4. **Database administration:** Mongo Express provides a web interface for inspecting MongoDB.
5. **Metrics collection:** cAdvisor collects container resource usage, and the MongoDB exporter exposes database statistics.
6. **Metrics storage:** Prometheus scrapes the configured targets and stores their metrics.
7. **Visualization:** Grafana connects to Prometheus and displays monitoring dashboards.

> **Networking note:** The browser accesses the API using `http://localhost:8000`. Containers communicate through their Compose service names. For example, the backend connects to MongoDB using `mongodb:27017`, while Grafana accesses Prometheus using `http://prometheus:9090`.

## Services and Responsibilities

| Service | Container Name | Host Port | Responsibility |
|---|---|---:|---|
| React + Nginx | `task_manager_frontend` | 3000 (container 8080) | Serves the web interface |
| FastAPI | `task_manager_api` | 8000 | Application API and `/metrics` |
| MongoDB | `task_manager_db` | 27017 | Stores application data |
| Mongo Express | `task_manager_mongo_ui` | 8081 | Database administration |
| MongoDB Exporter | `task_manager_mongo_exporter` | none (internal 9216) | Database metrics for Prometheus |
| cAdvisor | `task_manager_cadvisor` | 8082 (container 8080) | Container metrics |
| Prometheus | `task_manager_prometheus` | 9090 | Metrics collection and storage |
| Grafana | `task_manager_grafana` | 3001 (container 3000) | Monitoring dashboards |

Grafana is mapped to host port 3001 because host port 3000 is used by the frontend.

## Application Features

The Task Manager application is designed to support:

- Viewing the task list.
- Creating tasks.
- Updating task completion status.
- Deleting tasks.
- Storing tasks in MongoDB through the FastAPI backend.
- Communicating with the API through HTTP requests.

The exact functionality depends on the application code currently implemented.

## Project Structure

```text
kube/
├── Backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env
│   ├── database/
│   ├── models/
│   ├── routes/
│   └── services/
│
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── nginx.conf
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   └── src/
│
├── prometheus/
│   └── prometheus.yml
│
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── datasource.yml
│
├── docker-compose.yml
└── README.md
```

## Prerequisites

Install the following before running the project:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Docker Compose v2
- Git
- A modern web browser

Docker Desktop should be running before you execute Compose commands.

**Recommended resources:** at least 2 CPU cores and 4 GB of RAM available to Docker. With less memory, the stack starts slowly and health checks time out (see [Error 18](#error-18-slow-startup-and-timeouts-on-a-low-memory-host)).

## Getting Started

### 1. Clone the repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone <your-repository-url>
cd kube
```

### 2. Verify the configuration files

Ensure the project contains:

- `docker-compose.yml`
- `Backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- `prometheus/prometheus.yml`
- `grafana/provisioning/datasources/datasource.yml`

### 3. Validate the Docker Compose configuration

```bash
docker compose config --quiet
```

No output means the file is valid. Use `docker compose config` (without `--quiet`) to print the resolved configuration, including the final environment values each container receives.

### 4. Build and start the services

On a low-memory host, start the application first and the monitoring services afterwards:

```bash
docker compose up -d --build mongodb backend frontend mongo-express
docker compose up -d cadvisor prometheus grafana mongodb-exporter
```

On a machine with enough resources, one command is enough:

```bash
docker compose up -d --build
```

### 5. Check container status

```bash
docker compose ps
```

`task_manager_db` and `task_manager_api` should show `healthy`.

### 6. Inspect service logs

```bash
docker compose logs --tail=100 mongodb
docker compose logs --tail=100 backend
docker compose logs --tail=100 prometheus
docker compose logs --tail=100 grafana
```

For live logs from all services:

```bash
docker compose logs -f
```

## Accessing the Services

| Service | URL |
|---|---|
| Task Manager frontend | [http://localhost:3000](http://localhost:3000) |
| FastAPI API documentation | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Backend health endpoint | [http://localhost:8000/health](http://localhost:8000/health) |
| Backend metrics | [http://localhost:8000/metrics](http://localhost:8000/metrics) |
| Mongo Express | [http://localhost:8081](http://localhost:8081) |
| cAdvisor | [http://localhost:8082](http://localhost:8082) |
| Prometheus | [http://localhost:9090](http://localhost:9090) |
| Prometheus targets | [http://localhost:9090/targets](http://localhost:9090/targets) |
| Grafana | [http://localhost:3001](http://localhost:3001) |

Mongo Express is protected with the credentials configured in the Compose file. Grafana's admin login is set through the `GF_SECURITY_ADMIN_*` environment variables in the Compose file. Change the example passwords before sharing the project.

> **Important:** The browser origin of the frontend (`http://localhost:3000`) must be listed in the backend's CORS `allow_origins`. See [Error 5](#error-5-frontend-cannot-reach-the-backend-cors).

## Monitoring and Observability

### cAdvisor

cAdvisor exposes container-level metrics, including CPU usage, memory consumption, and container activity.

Open `http://localhost:8082`.

> **Known limitation on Docker Desktop:** cAdvisor can fail to identify individual containers when Docker Desktop uses the containerd image store, so it may report only the whole VM (`id="/"`). See [Error 12](#error-12-cadvisor-shows-only-the-whole-host).

### Backend metrics (FastAPI)

The backend uses `prometheus-fastapi-instrumentator` to expose request counts, latency, and status codes at `/metrics`.

Add to `Backend/requirements.txt`:

```text
prometheus-fastapi-instrumentator
```

Add to `Backend/main.py`:

```python
from prometheus_fastapi_instrumentator import Instrumentator

# after app = FastAPI(...) and app.include_router(...)
Instrumentator().instrument(app).expose(app)
```

### MongoDB exporter

MongoDB has no metrics endpoint of its own, so the Percona exporter connects to the database and exposes statistics on port 9216 for Prometheus. It is defined as the `mongodb-exporter` service in `docker-compose.yml` and uses the same root credentials as the database.

### Prometheus

Prometheus scrapes metrics from the targets listed in `prometheus/prometheus.yml`. The cAdvisor job uses a longer timeout because scrapes are slow on low-memory hosts.

```yaml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    scrape_interval: 60s
    scrape_timeout: 50s
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'backend'
    scrape_interval: 30s
    scrape_timeout: 20s
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'mongodb'
    scrape_interval: 30s
    scrape_timeout: 20s
    static_configs:
      - targets: ['mongodb-exporter:9216']
```

Prometheus only reads this file at startup. After editing it, run:

```bash
docker compose up -d --force-recreate prometheus
```

Open `http://localhost:9090/targets` and verify that every target is `UP`. In the query box, `up` returns one series per target, and `up == 0` lists only the failing ones.

### Grafana

Grafana visualizes metrics collected by Prometheus. The data source is created automatically from `grafana/provisioning/datasources/datasource.yml`.

1. Open `http://localhost:3001` and sign in.
2. Go to **Connections → Data sources** and confirm that **Prometheus** exists.
3. If it is missing, add it manually with the URL `http://prometheus:9090` (including `http://`, with no spaces).
4. Click **Save & test**.
5. Open **Explore** and run `up` to confirm data is flowing.
6. Import or build dashboards for the metrics you need.

Useful queries:

```text
up
mongodb_up
sum by (handler, status) (rate(http_requests_total[5m]))
histogram_quantile(0.95, sum by (le, handler) (rate(http_request_duration_seconds_bucket[5m])))
```

> **Monitoring scope:** cAdvisor provides container metrics where the host supports it, FastAPI instrumentation provides application-level metrics, and the MongoDB exporter provides database metrics.

## Errors Encountered and Fixes

Each entry lists the symptom, the root cause, and the fix applied during this project.

### Frontend build errors

#### Error 1: Build context disconnect (`/nginx.conf: not found`)

- **Symptom:** The build failed early with a `failed to compute cache key` error stating that `nginx.conf` or `package.json` paths could not be resolved.
- **Root cause:** A misunderstanding of the Docker build context. The build ran with the context set to the `frontend/` directory, but the Dockerfile used nested paths (such as `COPY ./frontend/package.json ./`) or tried to reach a file outside that folder. Docker cannot access files outside its defined context.
- **Fix:**
  1. Align the terminal's working directory (or the Compose `context:`) with the build context.
  2. Use paths relative to the context in the Dockerfile (`COPY . .` instead of repeating the folder name).

#### Error 2: Bloated cache and context transfer time (`npm ci` taking a long time)

- **Symptom:** The `[builder 4/6] RUN npm ci` step stalled and took a long time.
- **Root cause:** The build context included local host directories such as a large `node_modules` folder or build artifacts, which were uploaded to the Docker daemon. On the first run of a cache-mounted layer (`--mount=type=cache`), npm also performs a complete cold install over the network.
- **Fix:**
  1. Add an optimized `.dockerignore` that blocks the host's local `node_modules` and caches from being transferred.
  2. Use `--network=host` to bypass virtual network bridge overhead in Docker Desktop on Windows.
  3. Keep `--mount=type=cache,target=/root/.npm` so later builds reuse a persistent local cache instead of downloading from the registry again.

#### Error 3: Multi-stage artifact mismatch (`/app/dist: not found`)

- **Symptom:** The step `[runner 3/3] COPY --from=builder /app/dist` failed with a `not found` error at the end of the build.
- **Root cause:** The runner stage expected the output directory of a different build tool. The guide followed assumed Vite (output in `/app/dist`), but this project uses Create React App (`react-scripts`), which writes to `/app/build`.
- **Fix:** Change the artifact copy to match the compiler's output directory:

  ```dockerfile
  COPY --from=builder /app/build /usr/share/nginx/html
  ```

### Startup and connectivity errors

#### Error 4: MongoDB container is unhealthy

- **Symptom:**

  ```text
  Container task_manager_db  Error dependency mongodb failed to start
  dependency failed to start: container task_manager_db is unhealthy
  ```

- **Root cause:** MongoDB itself was running. The health check was failing:
  1. The first version piped `mongosh` output into `grep -q 'ok: 1'`, which is fragile because the output format varies.
  2. After removing `grep`, every check still ended with `Health check exceeded timeout`. Each check launched a full `mongosh` (Node.js) process, which took longer than the timeout on a slow, low-memory host, especially while images were being pulled and several containers started at once.
- **Fix:**
  1. Inspect the real result with `docker inspect --format='{{json .State.Health}}' task_manager_db`.
  2. Replace the `mongosh` check with a lightweight TCP check that returns in milliseconds, and allow a longer start period:

     ```yaml
     healthcheck:
       test: ["CMD-SHELL", "timeout 5 bash -c '</dev/tcp/127.0.0.1/27017'"]
       interval: 15s
       timeout: 10s
       retries: 10
       start_period: 60s
     ```

  3. The backend's `/health` endpoint still verifies the real database connection.

#### Error 5: Frontend cannot reach the backend (CORS)

- **Symptom:** The frontend showed "Could not connect to the backend", while `http://localhost:8000` opened fine directly in the browser.
- **Root cause:** CORS. The frontend was served from `http://localhost:8080`, but the backend's `allow_origins` only listed `http://localhost:3000` and `http://localhost:5173`. The browser blocked the cross-origin responses. Opening port 8000 directly is not a cross-origin request, so it worked.
- **Fix:**
  1. Serve the frontend on an allowed origin by mapping `"3000:8080"` in Compose (host 3000, container 8080), or add `http://localhost:8080` to `allow_origins`.
  2. Rebuild or recreate the affected container.
  3. Make the allowed origins configurable so they can change for Kubernetes:

     ```python
     import os

     origins = os.getenv(
         "CORS_ORIGINS",
         "http://localhost:3000,http://localhost:5173,http://localhost:8080",
     ).split(",")
     ```

  4. Verify with `curl -i -H "Origin: http://localhost:3000" http://localhost:8000/api/tasks` and look for `access-control-allow-origin`.
  5. Use `localhost`, not `127.0.0.1`. The browser treats them as different origins.

#### Error 6: Compose validation error (`additional properties 'cadvisor' not allowed`)

- **Symptom:**

  ```text
  validating docker-compose.yml: services.frontend additional properties 'cadvisor' not allowed
  ```

- **Root cause:** An indentation mistake. The `cadvisor:` block was pasted with extra indentation, so YAML read it as a setting inside `frontend:` instead of a separate service.
- **Fix:** Every service name must start at exactly 2 spaces under `services:`. Validate before applying with `docker compose config --quiet`.

#### Error 7: Port conflict between Grafana and the frontend

- **Symptom:** Grafana and the frontend both wanted host port 3000.
- **Root cause:** Grafana listens on port 3000 inside its container by default, and the frontend was moved to host port 3000.
- **Fix:** Map Grafana as `"3001:3000"` and open it at `http://localhost:3001`.

#### Error 8: Backend `/health` returns 503 and the backend is unhealthy

- **Symptom:** The backend started (`Uvicorn running`) but `GET /health` returned 503 and the container was marked unhealthy. The traceback ended with:

  ```text
  pymongo.errors.OperationFailure: Authentication failed.
  ```

- **Root cause:** `/health` returns 503 when the database connection check fails. MongoDB was reachable, but the password in the backend's `MONGO_URI` differed from the one MongoDB was initialised with. `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` are only applied on the first start with an empty volume, so later changes in the Compose file have no effect on an existing volume.
- **Fix:**
  1. Compare the passwords without printing them, using hashes:

     ```bash
     docker exec task_manager_api sh -c "printf '%s' \"\$MONGO_URI\" | sed -E 's#^[^:]+://[^:]+:([^@]*)@.*#\1#' | sha256sum"
     docker exec task_manager_db sh -c "printf '%s' \"\$MONGO_INITDB_ROOT_PASSWORD\" | sha256sum"
     ```

  2. Use the same password in all four places: `mongodb`, `mongo-express`, the `mongodb-exporter` command, and the backend `MONGO_URI`.
  3. If the stored user in the volume still differs, reset only the MongoDB volume (this deletes the tasks):

     ```bash
     docker compose down
     docker volume rm kube_mongo_data
     docker compose up -d mongodb
     ```

     Wait until `task_manager_db` is healthy, then run `docker compose up -d`.

#### Error 9: Backend crashes with `Invalid URI scheme`

- **Symptom:** The backend never started listening, the healthcheck got `Connection refused`, and the logs ended with:

  ```text
  pymongo.errors.InvalidURI: Invalid URI scheme: URI must begin with 'mongodb://' or 'mongodb+srv://'
  ```

- **Root cause:** A copy-and-paste error in the Compose file. The value contained the variable name twice, so the container received the literal text `MONGO_URI: mongodb://...`:

  ```yaml
  MONGO_URI: "MONGO_URI: mongodb://root:<password>@mongodb:27017/task_manager?authSource=admin"
  ```

  `database/connection.py` creates the `MongoClient` when the module is imported, so the app crashed before the server could start.
- **Fix:** The value must start directly with `mongodb://`:

  ```yaml
  MONGO_URI: "mongodb://root:<password>@mongodb:27017/task_manager?authSource=admin"
  ```

  Check the resolved value with `docker compose config | findstr MONGO_URI` (Windows) or `docker compose config | grep MONGO_URI`, then recreate the service with `docker compose up -d --force-recreate backend`. Use quotes only in the `KEY: value` style, never in the `- KEY=value` list style.

#### Error 10: Backend healthcheck too heavy for a slow host

- **Symptom:** The backend was marked unhealthy even though it was running, and the frontend (which waits for it) stayed in `Created`.
- **Root cause:** The healthcheck starts a Python process and calls `/health`, which also queries MongoDB. On a slow host, this exceeds short timeouts.
- **Fix:** Use the cheap liveness endpoint in the Docker healthcheck, and keep `/health` for full readiness checks (and later for Kubernetes readiness probes):

  ```yaml
  healthcheck:
    test:
      - CMD
      - python
      - -c
      - "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live', timeout=20)"
    interval: 30s
    timeout: 40s
    retries: 10
    start_period: 120s
  ```

### Monitoring errors

#### Error 11: Prometheus target `cadvisor` is DOWN (`context deadline exceeded`)

- **Symptom:** On the Targets page, `cadvisor` showed `DOWN` with `Get "http://cadvisor:8080/metrics": context deadline exceeded`.
- **Root cause:** The network path was fine. cAdvisor took about 10.7 seconds to answer, longer than the 10-second `scrape_timeout`. Even Prometheus scraping itself took about 3 seconds, which indicates a slow host.
- **Fix:**
  1. Give that job a longer interval and timeout (the timeout must not exceed the interval):

     ```yaml
     - job_name: 'cadvisor'
       scrape_interval: 60s
       scrape_timeout: 50s
     ```

  2. Reduce cAdvisor's work in Compose:

     ```yaml
     command:
       - --housekeeping_interval=30s
       - --disable_metrics=percpu,sched,tcp,udp,advtcp,hugetlb,referenced_memory,process
     ```

  3. Recreate Prometheus so it re-reads the file: `docker compose up -d --force-recreate prometheus`.

#### Error 12: cAdvisor shows only the whole host

- **Symptom:** `container_memory_usage_bytes` returned a single series with `id="/"`, and no `task_manager_*` containers appeared in Prometheus or Grafana. The cAdvisor logs were full of:

  ```text
  Failed to create existing container: /docker/<id>: failed to identify the read-write layer ID ...
  open /rootfs/var/lib/docker/image/overlayfs/layerdb/mounts/<id>/mount-id: no such file or directory
  ```

- **Root cause:** cAdvisor finds each container's cgroup, then looks up its storage layer under `/var/lib/docker/image/overlayfs/layerdb/`. On Docker Desktop with the containerd image store enabled, that directory does not exist, so cAdvisor drops every container and reports only the root cgroup. Flags and extra mounts cannot fix this.
- **Fix (choose one):**
  1. Disable **Use containerd for pulling and storing images** in Docker Desktop (Settings → General), restart, and rebuild the images. Back up any data you need first.
  2. Monitor the application instead of the container runtime: use FastAPI instrumentation (Error 14) and `docker stats` for per-container CPU and memory.
  3. Keep cAdvisor for whole-host CPU and memory only.

#### Error 13: Grafana cannot reach Prometheus (`connection refused` and `invalid URL`)

- **Symptom:** Grafana reported:

  ```text
  Post "http://localhost:9090/api/v1/query": dial tcp [::1]:9090: connect: connection refused
  ```

  After editing the URL, Grafana showed `Validation error, invalid URL`.
- **Root cause:**
  1. `localhost` inside the Grafana container is Grafana itself, not Prometheus. Containers reach each other by service name.
  2. Grafana rejects a URL without the `http://` scheme, or with stray spaces or characters.
- **Fix:** Set the data source URL to exactly `http://prometheus:9090`, typed by hand, then click **Save & test**. If the URL field is read-only, the data source comes from `grafana/provisioning/datasources/datasource.yml`. Correct the `url:` line there and recreate Grafana with `docker compose up -d --force-recreate grafana`.

#### Error 14: Prometheus has no metrics from the application containers

- **Symptom:** `up` listed only `prometheus` and `cadvisor`, and nothing from the backend, MongoDB, or other services.
- **Root cause:** Prometheus does not discover containers automatically. It scrapes only the targets in `prometheus.yml`, and each service must expose its own `/metrics` endpoint.
- **Fix:**
  1. Add `prometheus-fastapi-instrumentator` to the backend and expose `/metrics` (see [Backend metrics](#backend-metrics-fastapi)).
  2. Add the `mongodb-exporter` service, with credentials matching the database.
  3. Add `backend` and `mongodb` jobs to `prometheus.yml`.
  4. Rebuild the backend, then recreate Prometheus:

     ```bash
     docker compose up -d --build backend
     docker compose up -d --force-recreate prometheus
     ```

  5. Confirm every target is `1` in the `up` query or `UP` on the Targets page.

#### Error 15: Grafana shows "failed to load its application files"

- **Symptom:** Grafana's own error page appeared, listing proxy and sub-path suggestions.
- **Root cause:** The container was running and serving the page, so the failure was in the browser loading Grafana's JavaScript files. The usual causes are a stale browser cache, an ad-blocker or privacy extension, or a proxy rewriting asset requests.
- **Fix:**
  1. Open Grafana in an incognito window and hard refresh with Ctrl+Shift+R.
  2. Check the browser's Network tab for failing `/public/build/` files.
  3. If Docker runs on a remote machine or behind a proxy, set `GF_SERVER_ROOT_URL` to the address actually used.

### Environment errors

#### Error 16: Mongo Express and other services waiting on MongoDB

- **Symptom:** `docker compose up -d` printed `Container task_manager_db Waiting`, and dependent services stayed in `Created`.
- **Root cause:** This is expected behaviour. `depends_on` with `condition: service_healthy` holds dependent services until the database health check passes, and on a slow host the first start can take several minutes.
- **Fix:** Wait, and watch with `docker compose ps mongodb`. To work on one service in the meantime, start it without waiting: `docker compose up -d --no-deps backend`.

#### Error 17: Possible duplicate monitoring containers

- **Symptom:** Container names such as `cadvisor`, `prometheus`, and `grafana` appeared next to `task_manager_cadvisor` and similar names.
- **Root cause:** Older service definitions remained in the Compose file (or another Compose file in the project), so two sets of monitoring services were being created and competing for the same host ports.
- **Fix:** Keep one definition of each service, and check with `docker compose ps -a`.

#### Error 18: Slow startup and timeouts on a low-memory host

- **Symptom:** Everything was slow: MongoDB took about 17 seconds to create its storage engine, `mongosh` took more than 30 seconds to start, simple queries took seconds, and cAdvisor reported a Docker memory limit of about 2.8 GB at 86% usage.
- **Root cause:** On Windows, Docker Desktop runs containers in a hidden Linux VM (WSL2) with its own memory and CPU limits. With the default limits, MongoDB, Mongo Express, the backend, Prometheus, Grafana, and cAdvisor all competed for about 2.8 GB.
- **Fix:**
  1. Raise the VM limits in `C:\Users\<your-name>\.wslconfig`, leaving at least 2 GB for Windows:

     ```ini
     [wsl2]
     memory=4GB
     processors=4
     ```

     Then run `wsl --shutdown` and restart Docker Desktop.
  2. Start the services in stages (application first, monitoring second).
  3. Use lightweight health checks (Errors 4 and 10) and longer scrape timeouts (Error 11).
  4. Stop heavy optional services (`cadvisor`, `mongo-express`) when they are not needed.
  5. Keep the project inside the WSL filesystem rather than on a `C:\` path, because bind mounts from Windows drives are slow.

## Quick Troubleshooting Reference

| Problem | Check |
|---|---|
| A container is `unhealthy` | `docker inspect --format='{{json .State.Health}}' <container>` shows each check's real output |
| A container keeps restarting | `docker logs --tail 50 <container>` |
| Compose file rejected | `docker compose config --quiet`, and check indentation |
| Wrong environment value | `docker compose config` shows the resolved values |
| Frontend cannot reach the API | Browser dev tools → Network tab, and check CORS origins |
| Prometheus target down | `http://localhost:9090/targets` shows the exact scrape error |
| Grafana has no data | Explore → run `up`, and check the data source URL is `http://prometheus:9090` |
| Config change not applied | Recreate the service: `docker compose up -d --force-recreate <service>` |
| Need container CPU and memory quickly | `docker stats --no-stream` |

### Stop the services

```bash
docker compose down
```

This stops and removes the Compose containers and network while preserving named volumes.

**Avoid `docker compose down -v`** unless you intentionally want to delete the named persistent volumes and their stored data.


## Learning Outcomes

This project is intended to demonstrate practical experience with:

- Multi-stage Docker builds and understanding the Docker build context.
- Docker networking and service discovery.
- Docker Compose orchestration and dependency health checks.
- Persistent storage using Docker volumes.
- REST API deployment, CORS, and database integration.
- Infrastructure and application monitoring with cAdvisor, FastAPI instrumentation, exporters, and Prometheus.
- Grafana dashboards and metric queries.
- Troubleshooting container lifecycle, credentials, and service connectivity.
- Diagnosing resource limits on a Docker Desktop host.
- Preparing containerized applications for Kubernetes.

## Security Notes

This is a learning project, not a production-ready deployment.

- Replace example passwords with strong credentials, and keep them identical across every service that connects to MongoDB.
- Do not commit secrets or populated `.env` files to Git.
- Avoid exposing MongoDB, Mongo Express, Prometheus, cAdvisor, or Grafana publicly without appropriate access controls.
- Remove the `27017:27017` mapping if nothing outside Docker needs direct database access.
- cAdvisor runs as a privileged container with host paths mounted. Review container privileges and mounted host paths before deploying outside a local development environment.
- Passwords containing characters such as `@`, `:`, `/`, or `?` must be URL-encoded in `MONGO_URI`.

---

*Built as a hands-on infrastructure learning project, progressing from Docker Compose to Kubernetes with monitoring and observability.*
