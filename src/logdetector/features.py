"""Turn parsed log rows into numbers the model can use."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Bigger number = more serious
LEVEL_MAP = {"INFO": 1, "WARN": 2, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}


def build_features(df):
    """Return a matrix: level score, message length, and 5 TF-IDF keyword columns."""
    level_score = df["level"].map(LEVEL_MAP).fillna(1)   # unknown levels count as INFO
    msg_len = df["message"].apply(len)
    scalar_features = np.column_stack((level_score, msg_len))

    # TF-IDF turns rare words (like "refused") into numbers
    vectorizer = TfidfVectorizer(max_features=5, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["message"]).toarray()

    return np.hstack((scalar_features, tfidf_matrix))
