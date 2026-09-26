import re
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

def detect_log_anomalies(file_path="system_logs.txt"):
    # 1. Parse log file safely using Regex
    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+\[?(\w+)\]?\s+(.*)$")
    parsed_data = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                parsed_data.append(match.groups())

    df = pd.DataFrame(parsed_data, columns=["timestamp", "level", "message"])

    # 2. Extract Numerical + TF-IDF Text Features
    level_map = {"INFO": 1, "WARN": 2, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
    df["level_score"] = df["level"].map(level_map).fillna(1)
    df["msg_len"] = df["message"].apply(len)

    # TF-IDF converts rare log text keywords (e.g. "dump", "refused") into numbers
    vectorizer = TfidfVectorizer(max_features=5, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["message"]).toarray()

    # Merge scalar features and text features into matrix X
    scalar_features = df[["level_score", "msg_len"]].values
    X = np.hstack((scalar_features, tfidf_matrix))

    # 3. Fit Isolation Forest & calculate continuous anomaly scores
    model = IsolationForest(contamination=0.2, random_state=42)
    df["is_anomaly"] = model.fit_predict(X) == -1
    df["severity_score"] = model.decision_function(X)

    # Return detected anomalies sorted by severity (lowest score = highest severity)
    return df[df["is_anomaly"]].sort_values("severity_score")

if __name__ == "__main__":
    anomalies = detect_log_anomalies("system_logs.txt")
    print("🔍 Detected Anomalies:\n")
    print(anomalies[["timestamp", "level", "severity_score", "message"]])