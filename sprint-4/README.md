# Sprint 4 - Centralized Logging & Log Analytics

## Project Overview

This project implements a centralized logging pipeline using Docker Compose, Grafana Loki, Promtail, Grafana, and a sample web application.

## Components

* **Loki:** Stores centralized application logs.
* **Promtail:** Collects Docker container logs and extracts labels such as `container_name`, `level`, and `status_code`.
* **Grafana:** Visualizes and queries logs using Loki.
* **Sample Web App:** Generates structured JSON access and error logs.

## Start the Stack

Run the following command from the `sprint-4` directory:

```bash
docker-compose up -d --build
```

Check container status:

```bash
docker-compose ps
```

## Generate Sample Logs

```bash
curl http://localhost:5000/
curl http://localhost:5000/warn
curl http://localhost:5000/error
```

## View Logs in Grafana

Open Grafana at `http://localhost:3001`.

Go to **Explore**, select the **Loki** data source, and run this LogQL query:

```logql
{container_name="web-app"}
```

### Filter Logs by Level

```logql
{container_name="web-app", level="INFO"}
```

```logql
{container_name="web-app", level="WARN"}
```

```logql
{container_name="web-app", level="ERROR"}
```

The Grafana dashboard displays application log streams and refreshes automatically.

## Configuration Files

* `docker-compose.yml` - Defines the services.
* `loki.yml` - Configures Loki.
* `promtail.yml` - Configures Docker log collection and label extraction.
* `sample-app/` - Contains the sample web application and Dockerfile.
* `grafana/provisioning/` - Configures the Loki data source and dashboard provisioning.
* `grafana/dashboards/` - Contains the log dashboard definition.
