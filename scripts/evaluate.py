"""Measure how well a detector finds the injected problems in data/test.log.

Run from the project folder:
    PYTHONPATH=src python scripts/evaluate.py
"""
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score

from logdetector.model import detect_log_anomalies
from logdetector.parser import parse_lines

LOG_FILE = "data/test.log"
LABEL_FILE = "data/test_labels.csv"


def report(name, y_true, y_pred, kinds):
    """Print precision, recall and F1, plus how many of each kind of problem were caught."""
    print(f"\n=== {name} ===")
    print(f"flagged lines : {int(y_pred.sum())}")
    print(f"precision     : {precision_score(y_true, y_pred):.2f}   (of the lines flagged, how many were real problems)")
    print(f"recall        : {recall_score(y_true, y_pred):.2f}   (of the real problems, how many were found)")
    print(f"f1            : {f1_score(y_true, y_pred):.2f}")
    for kind in ["crash", "rare_message", "error_burst"]:
        mask = kinds == kind
        caught = int(y_pred[mask].sum())
        print(f"  {kind:<13}: caught {caught} of {int(mask.sum())}")


def main():
    lines = open(LOG_FILE, encoding="utf-8").readlines()
    labels = pd.read_csv(LABEL_FILE)
    df = parse_lines(lines)

    # every line must parse, otherwise line numbers no longer match the answer key
    assert len(df) == len(labels), "some log lines did not parse"

    y_true = labels["is_anomaly"].to_numpy()   # 1 = real problem
    kinds = labels["kind"].to_numpy()          # crash / rare_message / error_burst / normal

    # 1) the current detector (fits a new model on the data it scores)
    anomalies = detect_log_anomalies(lines)
    y_pred = df.index.isin(anomalies.index).astype(int)
    report("Current Isolation Forest (contamination 0.2)", y_true, y_pred, kinds)

    # 2) a plain rule: flag every ERROR and CRITICAL line
    y_rule = df["level"].isin(["ERROR", "CRITICAL"]).to_numpy().astype(int)
    report("Simple rule: level is ERROR or CRITICAL", y_true, y_rule, kinds)


if __name__ == "__main__":
    main()
