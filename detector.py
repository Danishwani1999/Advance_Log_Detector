import os
import re
import time
from collections import deque
from prometheus_client import Counter, Gauge, start_http_server

# Prometheus metrics
LOGS_PROCESSED = Counter('logs_processed_total', 'Total raw log lines processed from system file')
ANOMALIES_DETECTED = Counter('anomalies_detected_total', 'Total error-rate anomalies flagged by the detector')
ERROR_RATE_GAUGE = Gauge('log_error_rate', 'Proportion of error logs in the last processing window (0.0 - 1.0)')

LOG_FILE = os.getenv("LOG_FILE_PATH", "sample_system.log")
ERROR_THRESHOLD = float(os.getenv("ERROR_THRESHOLD", "0.3"))  # 30% errors in a window = anomaly
READ_FROM_START = os.getenv("READ_FROM_START", "false").lower() == "true"
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", "20"))  # number of most recent lines per window
MIN_SAMPLES = int(os.getenv("MIN_SAMPLES", "5"))  # don't judge a window with fewer lines
ERROR_PATTERN = re.compile(r"ERROR|CRITICAL|FATAL|EXCEPTION", re.IGNORECASE)


def is_error(line):
    """Return True if the log line looks like an error."""
    return bool(ERROR_PATTERN.search(line))


def error_rate(window):
    """Share of error lines in the window (0.0 - 1.0)."""
    return sum(window) / len(window) if window else 0.0


def process_log_stream():
    """Tail the log file continuously and update metrics."""
    if not os.path.exists(LOG_FILE):
        print(f"Waiting for log file {LOG_FILE} to be created...")
        time.sleep(3)
        return

    with open(LOG_FILE, "r") as f:
        if not READ_FROM_START:
            f.seek(0, os.SEEK_END)  # tail mode: only new lines

        window = deque(maxlen=WINDOW_SIZE)  # sliding window of the last N lines
        in_spike = False

        while True:
            line = f.readline()
            if not line:
                # No new line yet: sleep briefly and keep checking for appended logs
                time.sleep(1)
                continue

            LOGS_PROCESSED.inc()
            window.append(is_error(line))
            rate = error_rate(window)
            ERROR_RATE_GAUGE.set(rate)

            spiking = len(window) >= MIN_SAMPLES and rate >= ERROR_THRESHOLD
            if spiking and not in_spike:
                # Count one anomaly per spike, not one per line
                ANOMALIES_DETECTED.inc()
                print(f"[ALERT] Error spike detected! Window rate: {rate:.2f}")
            in_spike = spiking


if __name__ == "__main__":
    print("Starting Prometheus exporter on port 8000...")
    start_http_server(8000)
    print("Monitoring log stream for anomalies...")
    while True:
        try:
            process_log_stream()
        except Exception as e:
            print(f"Error encountered in log reader loop: {e}")
            time.sleep(3)
