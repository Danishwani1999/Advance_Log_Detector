"""Score log lines with an Isolation Forest and pick out the anomalies."""
from sklearn.ensemble import IsolationForest

from logdetector.features import build_features
from logdetector.parser import parse_lines


def detect_log_anomalies(lines):
    """Take raw log lines, return the anomalous ones (most severe first)."""
    df = parse_lines(lines)
    if df.empty:
        return df  # nothing parsed, so nothing to score

    X = build_features(df)

    # TODO (Step 4): replace this fixed 20% with a threshold learned from normal logs
    model = IsolationForest(contamination=0.2, random_state=42)
    df["is_anomaly"] = model.fit_predict(X) == -1
    df["severity_score"] = model.decision_function(X)  # lower = more unusual

    return df[df["is_anomaly"]].sort_values("severity_score")
