"""Turn raw log lines into a table."""
import re

import pandas as pd

# Matches: 2026-10-02 10:05:00 [CRITICAL] System crash detected (brackets optional)
LOG_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+\[?(\w+)\]?\s+(.*)$"
)


def parse_lines(lines):
    """Return a DataFrame with timestamp, level, message. Bad lines are skipped."""
    rows = []
    for line in lines:
        match = LOG_PATTERN.match(line.strip())
        if match:
            rows.append(match.groups())
    return pd.DataFrame(rows, columns=["timestamp", "level", "message"])
