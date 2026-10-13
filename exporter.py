mport time
import os
from prometheus_client import start_http_server, Counter, Gauge
from detector import LOG_FILE, parse_log_line, detect_anomalies

# Define Prometheus Metrics with Level Label
LOG_ANOMALIES_TOTAL = Counter(
    'log_anomalies_total', 
    'Total log anomalies detected', 
    ['level']
)
LOG_ANOMALY_SCORE = Gauge(
    'log_anomaly_score', 
    'Latest anomaly score evaluated', 
    ['level']
)

def tail_and_export():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("2026-10-13 10:00:00 [INFO] System initialized successfully.\n")

    with open(LOG_FILE, "r") as f:
        # Move to end of file for tail behavior
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(2)
                continue
            
            level, text = parse_log_line(line)
            results = detect_anomalies([(level, text)])
            
            for lvl, txt, score, is_anom in results:
                if is_anom:
                    LOG_ANOMALIES_TOTAL.labels(level=lvl).inc()
                LOG_ANOMALY_SCORE.labels(level=lvl).set(score)

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus Exporter started on port 8000...")
    tail_and_export()
