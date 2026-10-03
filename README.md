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

## 🏗 System Architecture

*The diagram below illustrates the ML anomaly scoring pipeline and Prometheus metric export flow:*

```mermaid
graph TD
    A[Log Files / Streams] --> B[detector.py: Log Parser & Isolation Forest Model]
    B -->|Anomaly Scores| C[exporter.py: Prometheus Metrics Exporter]
    C -->|Metrics Stream :8000| D[Prometheus Server]
    D --> E[Observability & Alerting Dashboard]
