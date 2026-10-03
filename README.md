# AIOps Log Anomaly Detection & Monitoring Pipeline

A real-time AIOps monitoring pipeline that detects anomalous system log entries using Python and exposes metric telemetry for scraping by Prometheus and visualization in Grafana.

---

## 🏗️️ Architecture & Monitoring Flow

```text
              System Logs
                   │
                   ▼
          Python Log Detector
                   │
                   ▼
         Anomaly Detection
                   │
                   ▼
          Prometheus Metrics
                   │
                   ▼
             Prometheus
                   │
                   ▼
               GrafanaComponentsLog Detector: Parses log streams, applies anomaly detection logic, and exposes custom Prometheus metrics on port 8000.Prometheus: Scrapes custom metrics from the Log Detector at regular intervals.Grafana: Pulls metric data from Prometheus to render dashboards and alerts.🚀 Getting StartedPrerequisitesDockerDocker ComposeRunning the StackTo start the entire monitoring stack in detached mode:Bashdocker compose up -d
📊 Project Output & Verification1. Docker Compose ServicesPlaintext$ docker compose ps

NAME                    STATUS
grafana_dashboard       Up
log_anomaly_detector    Up
prometheus_service      Up
2. Prometheus Health CheckVerify that the Prometheus server is live and healthy:Plaintext$ curl localhost:9090/-/healthy

Prometheus Server is Healthy.
3. Prometheus Target RegistrationThe log detector is configured as a Prometheus scrape target:Plaintextjob: log_detector_service
target: http://log-detector:8000/metrics
lastError: ""
4. Custom Application MetricsThe log detector exposes metrics on port 8000:Bashcurl localhost:8000/metrics
Key metric attributes:logs_processed_total: Total count of log lines processed.log_anomalies_total: Total count of detected anomalies.latest_anomaly_score: Statistical anomaly score assigned to the latest entry.Test Run Output:Plaintextlogs_processed_total 6.0
log_anomalies_total 2.0
latest_anomaly_score -0.009159840678413356
5. Log Anomaly Detection LogsPlaintextRunning log anomaly detection...
Prometheus metrics server is live on port 8000

[ALERT] Anomaly detected: System crash detected
✅ End-to-End Verification ChecklistService / Test ComponentStatusDocker Compose Setup✓Log Detector Service✓Prometheus Service✓Prometheus Scraping Target✓Custom Metrics Endpoint (:8000/metrics)✓Anomaly Detection Engine✓Grafana Dashboard Service✓
