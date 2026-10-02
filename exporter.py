import time
import tempfile
import os

from prometheus_client import start_http_server, Counter, Gauge
from detector import detect_log_anomalies


# Count total log lines processed
PROCESSED_LOGS = Counter(
    "logs_processed_total",
    "Total number of log lines analyzed by the detector"
)

# Count detected anomalies
ANOMALY_COUNT = Counter(
    "log_anomalies_total",
    "Total number of log anomalies detected"
)

# Store the latest anomaly score
ANOMALY_SCORE_GAUGE = Gauge(
    "latest_anomaly_score",
    "Anomaly score assigned to the most recent log line"
)


def process_new_logs(new_lines):
    """Analyze only newly added log lines."""

    if not new_lines:
        return

    temp_file = None

    try:
        # Create a temporary file containing only new log entries
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False
        ) as file:
            file.writelines(new_lines)
            temp_file = file.name

        # Run anomaly detection only on the new entries
        anomalies = detect_log_anomalies(temp_file)

        # Update Prometheus metrics
        PROCESSED_LOGS.inc(len(new_lines))

        for _, anomaly in anomalies.iterrows():
            ANOMALY_COUNT.inc()

            ANOMALY_SCORE_GAUGE.set(
                anomaly["severity_score"]
            )

            print(
                f"[ALERT] Anomaly detected: "
                f"{anomaly['message']}"
            )

    finally:
        # Remove temporary file
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def start_metrics_server(
    log_file_path="sample_system.log",
    poll_interval=3
):
    print("Starting log anomaly detector...")

    # Start Prometheus metrics server
    start_http_server(8000)

    print("Prometheus metrics server is live on port 8000")

    # Number of lines already processed
    processed_lines = 0

    while True:
        try:
            # Read current log file
            with open(
                log_file_path,
                "r",
                encoding="utf-8"
            ) as file:
                lines = file.readlines()

            current_line_count = len(lines)

            # Detect newly added lines
            if current_line_count > processed_lines:

                new_lines = lines[processed_lines:]

                print(
                    f"New log entries detected: "
                    f"{len(new_lines)}"
                )

                # Process ONLY the new lines
                process_new_logs(new_lines)

                # Remember processed lines
                processed_lines = current_line_count

            time.sleep(poll_interval)

        except Exception as error:
            print(f"Error processing logs: {error}")
            time.sleep(poll_interval)


if __name__ == "__main__":
    start_metrics_server()
