import time
import os
import re
from prometheus_client import start_http_server, Counter, Gauge

# Prometheus Metrics
LOGS_PROCESSED = Counter('logs_processed_total', 'Total raw log lines processed from system file')
ANOMALIES_DETECTED = Counter('anomalies_detected_total', 'Total error log anomalies flagged by rate detector')
ERROR_RATE_GAUGE = Gauge('log_error_rate', 'Current proportion of error logs in the last processing window (0.0 - 1.0)')

LOG_FILE = os.getenv("LOG_FILE_PATH", "sample_system.log")
ERROR_THRESHOLD = float(os.getenv("ERROR_THRESHOLD", "0.3"))  # 30% error threshold in window
ERROR_PATTERN = re.compile(r"ERROR|CRITICAL|FATAL|EXCEPTION", re.IGNORECASE)

def process_log_stream():
    """Tail and monitor log file for anomalous error rates without re-reading entire file."""
    if not os.path.exists(LOG_FILE):
        print(f"Waiting for log file {LOG_FILE} to be created...")
        return

    with open(LOG_FILE, 'r') as f:
        # Move to the end of file for streaming tail
        f.seek(0, os.SEEK_END)
        
        window_total = 0
        window_errors = 0
        
        while True:
            line = f.readline()
            if not line:
                # Calculate metric on window idle or pause
                if window_total > 0:
                    rate = window_errors / window_total
                    ERROR_RATE_GAUGE.set(rate)
                    if rate >= ERROR_THRESHOLD:
                        ANOMALIES_DETECTED.inc()
                        print(f"[ALERT] Error spike detected! Window rate: {rate:.2f}")
                    # Reset rolling window
                    window_total = 0
                    window_errors = 0
                
                time.sleep(1)
                continue

            LOGS_PROCESSED.inc()
            window_total += 1

            if ERROR_PATTERN.search(line):
                window_errors += 1

if __name__ == "__main__":
    print("Starting Prometheus Exporter on port 8000...")
    start_http_server(8000)
    print("Monitoring log stream for anomalies...")
    while True:
        try:
            process_log_stream()
        except Exception as e:
            print(f"Error encountered in log reader loop: {e}")
            time.sleep(3)
