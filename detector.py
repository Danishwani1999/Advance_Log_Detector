mport os
import time
import re
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

LOG_FILE = os.getenv("LOG_FILE_PATH", "sample_system.log")

def parse_log_line(line):
    # Extract log level (INFO, WARNING, ERROR, CRITICAL)
    match = re.search(r'\b(INFO|WARNING|ERROR|CRITICAL)\b', line)
    level = match.group(1) if match else "UNKNOWN"
    return level, line.strip()

def detect_anomalies(log_lines):
    if not log_lines:
        return []
    
    texts = [l[1] for l in log_lines]
    levels = [l[0] for l in log_lines]
    
    # Fallback if batch is too small for IsolationForest
    if len(texts) < 2:
        return [(lvl, txt, 0.0, 1 if lvl in ["ERROR", "CRITICAL"] else 0) for lvl, txt in log_lines]
    
    vectorizer = TfidfVectorizer(max_features=10)
    X = vectorizer.fit_transform(texts).toarray()
    
    # Use dynamic contamination safely
    clf = IsolationForest(contamination=0.1, random_state=42)
    preds = clf.fit_predict(X) # -1 for anomaly, 1 for normal
    
    results = []
    for i, txt in enumerate(texts):
        is_anomaly = 1 if preds[i] == -1 or levels[i] in ["ERROR", "CRITICAL"] else 0
        score = float(clf.decision_function(X[i].reshape(1, -1))[0])
        results.append((levels[i], txt, score, is_anomaly))
        
    return results
