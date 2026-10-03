# 🤖 AIOps Log Anomaly Detection & Monitoring Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![OS](https://img.shields.io/badge/Ubuntu-Linux-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

An end-to-end AIOps monitoring pipeline that ingests system log streams, computes statistical anomaly scores in real time using Python, exposes custom metric endpoints, and integrates seamlessly with Prometheus and Grafana for full-stack observability.

---

## 📌 Table of Contents

- [Features](#-features)
- [Architecture & Data Flow](#-architecture--data-flow)
- [Tech Stack](#-tech-stack)
- [Quick Start Guide (Ubuntu)](#-quick-start-guide-ubuntu)
- [Project Verification & Operational Outputs](#-project-verification--operational-outputs)
- [Metrics Specification](#-metrics-specification)
- [System Checklist](#-system-checklist)
- [Git Workflow](#-git-workflow)

---

## ✨ Features

* **Real-time Anomaly Detection**: Continuously parses system log streams and tags critical events.
* **Prometheus Telemetry Integration**: Exposes custom application metrics over an HTTP exporter endpoint (`:8000/metrics`).
* **Containerized Microservices**: Fully orchestrated using Docker Compose for isolated and reproducible deployments.
* **Automated Health Monitoring**: Integrated Prometheus scrape target with sub-second metrics updating.
* **Interactive Visualization**: Ready for Grafana dashboard rendering and real-time alert triggers.

---

## 🏗️ Architecture & Data Flow

```text
       ┌───────────────┐
       │  System Logs  │
       └───────┬───────┘
               │
               ▼
┌─────────────────────────────┐
│    Python Log Detector      │
│  (Anomaly Engine & Exporter)│
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Prometheus Metrics Endpoint │
│  (http://localhost:8000)    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Prometheus Server      │
│   (Metrics Collection)      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Grafana Dashboard      │
│  (Visualization & Alerting) │
└──────────────┬──────────────┘



🛠️ Tech StackDomainTechnologyDescriptionLanguagePython 3Core log parsing and anomaly detection logicTelemetry ExporterPrometheus Client LibraryCustom HTTP server exposing metric counters/gaugesMetrics StoragePrometheusTime-series database scraping target endpointsVisualizationGrafanaOperational dashboards and analytical chartsContainerizationDocker & Docker ComposeMulti-container environment orchestrationOperating SystemUbuntu LinuxTarget development and deployment environment🚀 Quick Start Guide (Ubuntu)1. Prerequisites InstallationEnsure Docker and Docker Compose are installed on your Ubuntu machine:Bash# Update package indices
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose plugin
sudo apt install -y docker.io docker-compose-v2

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Allow current user to run Docker without sudo
sudo usermod -aG docker $USER
2. Launch the Monitoring StackStart all microservices in detached mode:Bashdocker compose up -d
3. Service Access MatrixServiceExposed PortURL / EndpointLog Detector Exporter8000http://localhost:8000/metricsPrometheus Server9090http://localhost:9090Grafana Dashboard3000http://localhost:3000📊 Project Verification & Operational Outputs1. Docker Compose Services StatusBash$ docker compose ps
Output:PlaintextNAME                    STATUS
grafana_dashboard       Up
log_anomaly_detector    Up
prometheus_service      Up
2. Prometheus Server Health CheckBash$ curl localhost:9090/-/healthy
Output:PlaintextPrometheus Server is Healthy.
3. Target Scrape RegistrationScrape status verified via Prometheus API / Target configuration:YAMLjob: log_detector_service
target: http://log-detector:8000/metrics
health: UP
lastError: ""
4. Custom Application Telemetry EndpointBash$ curl localhost:8000/metrics
Exposed Metrics Sample Output:Plaintext# HELP logs_processed_total Total count of log lines processed
# TYPE logs_processed_total counter
logs_processed_total 6.0

# HELP log_anomalies_total Total count of detected anomalous log events
# TYPE log_anomalies_total counter
log_anomalies_total 2.0

# HELP latest_anomaly_score Statistical score of the most recently processed log entry
# TYPE latest_anomaly_score gauge
latest_anomaly_score -0.009159840678413356
5. Detector Engine Execution LogsBash$ docker compose logs log_anomaly_detector
Output:PlaintextRunning log anomaly detection...
Prometheus metrics server is live on port 8000

[ALERT] Anomaly detected: System crash detected
📈 Metrics SpecificationMetric NameTypeDescriptionlogs_processed_totalCounterMonotonically increasing counter tracking total logs read.log_anomalies_totalCounterTracks total number of anomalous events detected.latest_anomaly_scoreGaugeDynamic float value reflecting the confidence score of the last entry.✅ System Checklist[x] Docker Compose multi-service deployment[x] Python log stream parser & anomaly detection engine[x] Custom Prometheus HTTP exporter on port 8000[x] Prometheus automated scrape job configuration[x] Real-time anomaly detection verified with test logs[x] Grafana service live and connected📄 LicenseThis project is open-source and available under the MIT License.
