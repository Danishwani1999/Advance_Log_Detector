"""Watch the log file and publish Prometheus metrics."""
import time

from prometheus_client import Counter, Gauge, start_http_server

from logdetector import config
from logdetector.model import detect_log_anomalies

# Count total log lines processed
PROCESSED_LOGS = Counter(
    "logs_processed_total",
    "Total number of log lines analyzed by the detector",
)

# Count detected anomalies
ANOMALY_COUNT = Counter(
    "log_anomalies_total",
    "Total number of log anomalies detected",
)

# Store the latest anomaly score
ANOMALY_SCORE_GAUGE = Gauge(
    "latest_anomaly_score",
    "Anomaly score assigned to the most recent log line",
)


def process_new_logs(new_lines):
    """Analyze only the newly added lines and update the metrics."""
    if not new_lines:
        return

    # The detector takes lines directly now, so no temp file is needed
    anomalies = detect_log_anomalies(new_lines)

    PROCESSED_LOGS.inc(len(new_lines))

    for _, anomaly in anomalies.iterrows():
        ANOMALY_COUNT.inc()
        ANOMALY_SCORE_GAUGE.set(anomaly["severity_score"])
        print(f"[ALERT] Anomaly detected: {anomaly['message']}")


def start_metrics_server(log_file_path=config.LOG_FILE, poll_interval=config.POLL_INTERVAL):
    print("Starting log anomaly detector...")

    # Start the Prometheus metrics server
    start_http_server(config.METRICS_PORT)
    print(f"Prometheus metrics server is live on port {config.METRICS_PORT}")

    # How many lines we have already processed
    processed_lines = 0

    while True:
        try:
            # Read the current log file
            with open(log_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            current_line_count = len(lines)

            # Look for newly added lines
            if current_line_count > processed_lines:
                new_lines = lines[processed_lines:]
                print(f"New log entries detected: {len(new_lines)}")

                # Process ONLY the new lines
                process_new_logs(new_lines)

                # Remember how far we got
                processed_lines = current_line_count

            time.sleep(poll_interval)

        except Exception as error:
            print(f"Error processing logs: {error}")
            time.sleep(poll_interval)


if __name__ == "__main__":
    start_metrics_server()
