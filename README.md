# 🕵️‍♂️ Advance Log Detector

![Build Status](https://img.shields.io/badge/build-passing-success)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Prometheus](https://img.shields.io/badge/prometheus-monitored-orange)
![License](https://img.shields.io/badge/license-MIT-green)

> An AIOps log anomaly detection tool powered by Machine Learning (`IsolationForest`) with built-in Prometheus observability metrics and Docker support.

---

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Docker Setup (Recommended)](#docker-setup-recommended)
  - [Local Setup](#local-setup)
- [Verifying Metrics & Observability](#-verifying-metrics--observability)
- [Testing & Synthetic Anomaly Generation](#-testing--synthetic-anomaly-generation)
- [Configuration](#️-configuration)
- [How It Works Under the Hood](#-how-it-works-under-the-hood)
- [License](#-license)

---

## 📖 About the Project
Traditional log analysis relies on static regex rules and hardcoded threshold alerts that flood engineers with false positives while missing unknown failure patterns.

**Advance Log Detector** is an AI-assisted AIOps solution that uses unsupervised Machine Learning (`IsolationForest`) to parse system logs, extract text vectors, score anomalies automatically, and export real-time metrics directly to **Prometheus**.

---

## 🏗️ System Architecture

*The diagram below illustrates the ML anomaly scoring pipeline and Prometheus metric export flow:*

```mermaid
graph TD
    A[Log Files / Streams] --> B[detector.py: Log Parser & Isolation Forest Model]
    B -->|Anomaly Scores| C[exporter.py: Prometheus Metrics Exporter]
    C -->|Metrics Stream :8000| D[Prometheus Server]
    D --> E[Observability & Alerting Dashboard]
✨ Key Features
Unsupervised ML Scoring: Uses scikit-learn Isolation Forest to flag rare log anomalies without requiring labeled training datasets.

Prometheus Observability: Exposes real-time anomaly metrics on port 8000 for scraping by Prometheus.

Container Ready: Fully containerized with a Dockerfile and docker-compose.yml for quick deployment.

Data Preprocessing: Leverages pandas to structure raw text log entries before feeding them to the anomaly model.

🛠️ Tech Stack
Language: Python 3.9+

Data & Machine Learning: pandas, scikit-learn (IsolationForest)

Observability: prometheus-client, Prometheus

DevOps & Infrastructure: Docker, Docker Compose

📁 Project Structure
Plaintext
Advance_Log_Detector/
├── detector.py          # Core log parsing & Isolation Forest anomaly detection engine
├── exporter.py          # Prometheus metrics exporter (:8000/metrics)
├── sample.log           # Sample log dataset for local testing
├── Dockerfile           # Application container image configuration
├── docker-compose.yml   # Multi-container setup (Detector + Prometheus)
├── prometheus.yml       # Prometheus scraping configuration
├── requirements.txt     # Python dependencies (pandas, scikit-learn, prometheus-client)
├── .gitignore
└── README.md            # Project documentation
🚀 Getting Started
Prerequisites
Docker & Docker Compose OR Python 3.9+ installed locally.

Docker Setup (Recommended)
Bash
# 1. Clone the repository
git clone git@github.com:Danishwani1999/Advance_Log_Detector.git

# 2. Move into project directory
cd Advance_Log_Detector

# 3. Build and launch application & Prometheus containers
docker-compose up --build
Local Setup
Bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install required libraries
pip install -r requirements.txt

# 4. Run anomaly detection on sample logs
python detector.py

# 5. Start Prometheus metrics exporter
python exporter.py
📊 Verifying Metrics & Observability
Once exporter.py or Docker Compose is running:

Prometheus Metrics Stream: Open http://localhost:8000 in your browser to view raw metrics published by exporter.py.

Prometheus Target UI: Open http://localhost:9090 to query metrics via PromQL (e.g., log_anomalies_total).

🧪 Testing & Synthetic Anomaly Generation
Want to test the detector in real time? Append a synthetic error or brute-force pattern to sample.log:

Bash
# Append an anomalous log entry to trigger the ML detector
echo "2026-10-03 11:40:00 [CRITICAL] Authentication bypass attempt detected from IP 192.168.1.99" >> sample.log

# Re-run the detector to verify the anomaly score spike
python detector.py
⚙️ Configuration
Key model settings inside detector.py:

contamination: Sensitivity threshold for IsolationForest (default: 0.05 / top 5% flagged as anomalies).

max_features: TF-IDF feature extraction dimensions.

sample_log_path: Path to target log file stream (default: ./sample.log).

🧠 How It Works Under the Hood
Feature Extraction: Log lines are loaded using pandas and transformed into numeric feature vectors using TF-IDF / structured feature encoding.

Anomaly Isolation: IsolationForest randomly partitions feature values. Because anomalous log events (like sudden kernel panics or brute-force floods) are rare and distinct, they require fewer splits to isolate, yielding higher anomaly scores.

Metric Exporting: exporter.py runs a lightweight HTTP server publishing metrics (e.g., total log count, anomaly count, threat levels) that Prometheus scrapes periodically.

📄 License
Distributed under the MIT License. See LICENSE for more details.

Developed by Danish Wani
