### settings for the log detector, read from environment variables."""
import os

# Which log file to watch (the default matches your current Docker mount)
LOG_FILE = os.getenv("LOG_FILE", "sample_system.log")

# How many seconds to wait between checks for new lines
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "3"))

# Port where Prometheus metrics are served
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))
