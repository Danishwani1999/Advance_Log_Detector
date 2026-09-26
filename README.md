## AIOps Log Anomaly Detector

A lightweight log analysis tool built for modern DevOps pipelines. Instead of relying on rigid, hardcoded rules, this script combines Regex line parsing, TF-IDF text analysis, and Isolation Forest machine learning to automatically detect and rank unusual server log events.

## Why This Project?

Traditional log monitoring alerts on fixed triggers (like level == "ERROR"). However, rare system failures, silent timeouts, and unknown error messages often slip through static filters.

This project treats log monitoring as an unsupervised anomaly detection problem—converting raw log text into numerical features so an ML model can spot unexpected behaviors on its own.

## How It Works

Raw Log File --> Regex Extraction --> TF-IDF Text Vectorization --> Isolation Forest ML --> Severity-Ranked Alerts

Safe Parsing: Uses regular expressions (re) to quietly ignore malformed lines and reliably extract timestamps, log levels, and messages.

Feature Fusion: Combines scalar metrics (log level severity score and message length) with TF-IDF vectors that capture rare message keywords ("timeout", "refused", "dump").

Anomaly Scoring: Trains an Isolation Forest model on the feature matrix and uses decision_function() to assign continuous severity scores rather than binary flags.

Prerequisites
Python 3.8+
