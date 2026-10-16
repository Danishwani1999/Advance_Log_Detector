# Advance Log Detector

Log error-rate detector that exposes Prometheus metrics, with provisioned Grafana dashboard and alert rules (Docker Compose).
Detection is threshold-based: the error rate is compared to ERROR_THRESHOLD (default 0.3). No ML is used.

Author: Danish Wani

## Architecture
    data/sample_system.log -> detector (:8000/metrics) -> Prometheus (:9090, alert_rules.yml) -> Grafana (:3000)

## Services
| Service | Port (localhost) | Notes |
|---|---|---|
| detector | 8000 | non-root user, HEALTHCHECK, read-only log mount |
| prometheus | 9090 | v2.47.0, persistent volume, 15d retention, alert rules |
| grafana | 3000 | v10.1.0, provisioned datasource/dashboard, persistent volume |

## Run
    cp .env.example .env     # set GRAFANA_ADMIN_PASSWORD
    docker compose up -d --build
    curl localhost:8000/metrics
    curl localhost:9090/-/healthy

## Config (env vars on detector)
LOG_FILE_PATH, ERROR_THRESHOLD, READ_FROM_START

## CI
GitHub Actions: syntax check, compose validation, image build, promtool config/rule check.

## Next steps
Alertmanager, unit tests for detector, multiple log formats.
