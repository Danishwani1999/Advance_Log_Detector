import time
import os
from prometheus_client import start_http_server, Counter
from src.logdetector.config import LOG_FILE_PATH, METRIC_PORT, POLL_INTERVAL
from src.logdetector.parser import parse_log_line

# Define Prometheus counter metric
LOGS_PROCESSED = Counter('log_lines_processed_total', 'Total log lines processed', ['level'])

def tail_logs():
    print(f"Starting log exporter on port {METRIC_PORT}, monitoring {LOG_FILE_PATH}")
    start_http_server(METRIC_PORT)
    
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Warning: Log file {LOG_FILE_PATH} not found. Waiting for it to appear...")

    while True:
        if not os.path.exists(LOG_FILE_PATH):
            time.sleep(POLL_INTERVAL)
            continue

        try:
            with open(LOG_FILE_PATH, 'r') as f:
                # Read lines and increment Prometheus counters
                for line in f:
                    level = parse_log_line(line)
                    LOGS_PROCESSED.labels(level=level).inc()
                    
            time.sleep(POLL_INTERVAL)
        except Exception as e:
            print(f"Error reading log file: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    tail_logs()
