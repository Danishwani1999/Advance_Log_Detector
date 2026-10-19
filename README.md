# Advance Log Detector

Log error-rate detector that exposes Prometheus metrics. Alert rules fire through Alertmanager to a webhook receiver, and Grafana has a provisioned dashboard. Everything runs with Docker Compose.

## How it works

1. `detector.py` reads the log file at `LOG_FILE_PATH`, parses lines with regex, and tracks the error rate.
2. It exposes metrics on port 8000 using `prometheus_client`.
3. Prometheus scrapes `detector:8000` and evaluates `alert_rules.yml`.
4. Firing alerts go to Alertmanager (9093), which posts to the `alert-webhook` service.
5. Grafana loads its datasource and dashboard from `grafana/provisioning` and `grafana/dashboards`.

## Services

| Service | Port | Purpose |
|---|---|---|
| detector | 8000 | Metrics endpoint |
| prometheus | 9090 | Scraping and alert rules |
| alertmanager | 9093 | Alert routing |
| alert-webhook | internal | Alert receiver |
| grafana | 3000 | Dashboard |

## Configuration (detector)

| Variable | Default | Meaning |
|---|---|---|
| LOG_FILE_PATH | /data/sample_system.log | Log file to read |
| ERROR_THRESHOLD | 0.3 | Error-rate threshold |
| READ_FROM_START | true | Read the file from the beginning |

## Run and test

    docker compose up -d --build
    pytest
    flake8

## Verified output

`docker compose ps`
```
NAME                                   IMAGE                           COMMAND                  SERVICE         CREATED          STATUS                    PORTS
advance_log_detector-alert-webhook-1   mendhak/http-https-echo:31      "docker-entrypoint.s…"   alert-webhook   35 seconds ago   Up 25 seconds             8080/tcp, 8443/tcp
advance_log_detector-alertmanager-1    prom/alertmanager:v0.26.0       "/bin/alertmanager -…"   alertmanager    30 seconds ago   Up 23 seconds             0.0.0.0:9093->9093/tcp, [::]:9093->9093/tcp
advance_log_detector-detector-1        advance_log_detector-detector   "python -u detector.…"   detector        35 seconds ago   Up 25 seconds (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
advance_log_detector-grafana-1         grafana/grafana:10.1.0          "/run.sh"                grafana         26 seconds ago   Up 20 seconds             0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp
advance_log_detector-prometheus-1      prom/prometheus:v2.47.0         "/bin/prometheus --c…"   prometheus      27 seconds ago   Up 22 seconds             0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp
```

`curl localhost:8000/metrics` (custom metrics)
```
# HELP logs_processed_total Total raw log lines processed from system file
# TYPE logs_processed_total counter
logs_processed_total 42.0
# HELP anomalies_detected_total Total error-rate anomalies flagged by the detector
# TYPE anomalies_detected_total counter
anomalies_detected_total 1.0
# HELP log_error_rate Proportion of error logs in the last processing window (0.0 - 1.0)
# TYPE log_error_rate gauge
log_error_rate 0.30952380952380953
```

`Prometheus targets`
```
log_detector_service http://detector:8000/metrics up
```

## Screenshots





















## Author

Danish Ahmad Wani
