# Sprint 1 - Observability & System Monitoring

## Project
Local monitoring stack using Docker Compose, Prometheus, Node Exporter, and Grafana.

## Components
- Prometheus - collects and stores metrics
- Node Exporter - provides host system metrics
- Grafana - visualizes the metrics

## Setup

Start the monitoring stack:

docker-compose up -d

Check running containers:

docker-compose ps

## Access URLs

Prometheus:
http://localhost:9090

Grafana:
http://localhost:3000

## Grafana Dashboard

The dashboard displays:
- CPU Utilization
- RAM Usage
- Disk Usage

## Metrics

Prometheus automatically scrapes metrics from Node Exporter at:

http://node-exporter:9100/metrics
