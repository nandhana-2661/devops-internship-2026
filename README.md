# Sprint 1 - Observability & System Monitoring

## Project Overview

This project implements a local observability and system monitoring stack using Docker Compose, Prometheus, Node Exporter, and Grafana.

The system collects host-level metrics and visualizes CPU utilization, RAM usage, and disk usage through a Grafana dashboard.

## Architecture

The monitoring flow is:

Node Exporter → Prometheus → Grafana

- Node Exporter collects host system metrics.
- Prometheus scrapes and stores the metrics.
- Grafana connects to Prometheus and visualizes the metrics.

## Components

### Prometheus
Collects and stores metrics from Node Exporter.

### Node Exporter
Provides host system metrics such as CPU, memory, and filesystem information.

### Grafana
Visualizes the collected metrics through a monitoring dashboard.

## Prerequisites

- Docker
- Docker Compose
- Linux/WSL environment

## Project Structure

sprint-1/
├── docker-compose.yml
├── prometheus.yml
├── README.md
└── screenshots/
    ├── docker-compose-ps.png
    └── grafana-dashboard.png

## Setup

Start the monitoring stack:

docker-compose up -d

Check the running containers:

docker-compose ps

## Prometheus Configuration

Prometheus is configured to scrape Node Exporter every 15 seconds.

Node Exporter target:

http://node-exporter:9100/metrics

## Grafana Configuration

Prometheus is configured as the Grafana data source using:

http://prometheus:9090

The Grafana dashboard displays:

- CPU Utilization
- RAM Usage
- Disk Usage

## Persistence

Named Docker volumes are used to persist Prometheus and Grafana data across container restarts.

Volumes:

- prometheus_data
- grafana_data

## Access URLs

Prometheus:

http://localhost:9090

Grafana:

http://localhost:3000

## Verification

Check the container status:

docker-compose ps

Verify Prometheus targets:

curl http://localhost:9090/api/v1/targets

The Node Exporter target should show a healthy/up status.

## Design Decisions

Docker Compose was used to run all monitoring components together.

Prometheus was selected for metrics collection and storage, Node Exporter for host-level metrics, and Grafana for visualization.

Named Docker volumes were used to ensure monitoring data and Grafana configuration persist across container restarts.

## Proof of Work

Screenshots are provided in the screenshots directory:

- docker-compose-ps.png - running container status
- grafana-dashboard.png - Grafana dashboard showing CPU, RAM, and Disk metrics
