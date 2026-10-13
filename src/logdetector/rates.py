"""Count how many errors happened recently (a sliding 60-second window)."""
import pandas as pd

WINDOW = "60s"
ERROR_LEVELS = ["ERROR", "CRITICAL"]


def recent_error_counts(is_error, times):
    # Create Series, set datetime index, and sort it to make it monotonic
    s = pd.Series(is_error, index=pd.DatetimeIndex(times))
    s = s.sort_index()
    s = s[~s.index.duplicated(keep="first")]
    return s.rolling(WINDOW).sum().to_numpy()
