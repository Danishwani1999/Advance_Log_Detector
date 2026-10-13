"""Learn what normal logs look like and save it.

Run from the project folder:
    PYTHONPATH=src python scripts/train.py
"""
import os

import joblib

from logdetector import config
from logdetector.model import train

BASELINE_FILE = "data/baseline.log"


def main():
    lines = open(BASELINE_FILE, encoding="utf-8").readlines()
    bundle = train(lines)

    os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)
    joblib.dump(bundle, config.MODEL_PATH)

    print(f"learned {len(bundle['counts'])} normal message types from {len(lines)} lines")
    print(f"error-rate limit: more than {bundle['rate_limit']} errors in 60 seconds is unusual")
    print(f"saved to {config.MODEL_PATH}")


if __name__ == "__main__":
    main()
