import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Unified configuration via environment variables with safe defaults
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", str(BASE_DIR / "data" / "sample_system.log"))
METRIC_PORT = int(os.getenv("METRIC_PORT", 8000))
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", 3.0))
