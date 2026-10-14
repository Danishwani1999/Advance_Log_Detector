import os
import re
import time

from prometheus_client import Counter, Gauge, start_http_server

# Prometheus metrics
LOGS_PROCESSED = Counter('logs_processed_total', 'Total raw log lines processed from system file')
ANOMALIES_DETECTED = Counter('anomalies_detected_total', 'Total error-rate anomalies flagged by the detector')
ERROR_RATE_GAUGE = Gauge('log_error_rate', 'Proportion of error logs in the last processing window (0.0 - 1.0)')

LOG_FILE = os.getenv("LOG_FILE_PATH", "sample_system.log")
ERROR_THRESHOLD = float(os.getenv("ERROR_THRESHOLD", "0.3"))  # 30% errors in a window = anomaly
READ_FROM_START = os.getenv("READ_FROM_START", "false").lower() == "true"
ERROR_PATTERN = re.compile(r"ERROR|CRITICAL|FATAL|EXCEPTION", re.IGNORECASE)


def process_log_stream():
    """Tail the log file and flag windows whose error rate crosses the threshold."""
    if not os.path.exists(LOG_FILE):
        print(f"Waiting for log file {LOG_FILE} to be created...")
        time.sleep(3)
        return

    with open(LOG_FILE, "r") as f:
        if not READ_FROM_START:
            f.seek(0, os.SEEK_END)  # tail mode: only new lines

        window_total = 0
        window_errors = 0

        while True:
            line = f.readline()
            if not line:
                # No new data: evaluate the window we just collected
                if window_total > 0:
                    rate = window_errors / window_total
                    ERROR_RATE_GAUGE.set(rate)
                    if rate >= ERROR_THRESHOLD:
                        ANOMALIES_DETECTED.inc()
                        print(f"[ALERT] Error spike detected! Window rate: {rate:.2f}")
                    window_total = 0
                    window_errors = 0
                time.sleep(1)
                continue

            LOGS_PROCESSED.inc()
            window_total += 1
            if ERROR_PATTERN.search(line):
                window_errors += 1


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
