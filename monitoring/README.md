# Karaoke-Inator Telemetry with OpenTelemetry

This directory contains configuration for OpenTelemetry (OTEL) distributed tracing stack for local development.

## Quick Start

### 1. Start the OTEL Stack

```bash
# From the project root
docker-compose -f docker-compose.yml -f docker-compose.otel.yml up -d
```

### 2. Access Grafana

- **URL**: http://localhost:3000
- **Username**: admin
- **Password**: admin

### 3. View Traces

Go to Grafana > Explore > select "Tempo" datasource to see distributed traces from your services.

### 4. Stop the Stack

```bash
docker-compose -f docker-compose.yml -f docker-compose.otel.yml down
```

## Stack Components

- **OTEL Collector**: Receives telemetry from services (port 4317 for gRPC)
- **Tempo**: Trace storage backend (3-month retention)
- **Prometheus**: Metrics storage (90-day retention)
- **Grafana**: Unified visualization dashboard

## Configuration Files

- `otel-collector-config.yaml` - OTEL Collector receiver, processor, and exporter config
- `tempo-config.yaml` - Tempo trace storage settings
- `prometheus-otel.yml` - Prometheus scrape configuration for OTEL metrics
- `grafana-datasources-otel.yaml` - Grafana datasource definitions (Tempo, Prometheus)
- `grafana-dashboards.yaml` - Grafana dashboard provisioning
- `grafana-dashboards/` - Dashboard JSON files

## Service Integration

All backend services (orchestrator, voice-separation, lyrics-extraction, song-management) are instrumented with OpenTelemetry SDK to send traces to the OTEL Collector on port 4317.

See root-level `OTEL_SETUP.md` for full instrumentation details.
