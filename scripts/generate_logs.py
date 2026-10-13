"""Make fake but realistic log files so we can measure the detector.

Creates:
  data/baseline.log     - normal logs only (the model learns from this later)
  data/test.log         - normal logs plus injected problems
  data/test_labels.csv  - which lines of test.log are real problems
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # same numbers every run, so results can be repeated

# How often each level shows up in normal traffic
LEVEL_WEIGHTS = {"INFO": 92, "WARN": 6, "ERROR": 2}

# Normal messages per level, with how often each appears
NORMAL = {
    "INFO": [
        ("User login successful", 30),
        ("Health check passed", 25),
        ("Database connection established", 10),
        ("Cache refreshed", 10),
        ("Scheduled backup job completed", 5),
        ("Request processed successfully", 30),
    ],
    "WARN": [
        ("High memory usage detected", 5),
        ("Slow response from payment API", 5),
        ("Disk usage above 75 percent", 3),
    ],
    "ERROR": [
        ("Request timeout while calling external service", 2),
        ("Failed to send email, will retry", 2),
    ],
}

# Messages the system has never produced before (203.0.113.x is a safe example IP range)
RARE_MESSAGES = [
    ("ERROR", "Unauthorized root login attempt from 203.0.113.50"),
    ("ERROR", "Kernel panic: unable to mount root filesystem"),
    ("CRITICAL", "Out of memory: killed process 4312"),
    ("INFO", "Admin privileges granted to user guest_7731"),
    ("WARN", "Configuration file modified outside deployment window"),
    ("INFO", "Outbound connection opened to 198.51.100.23 on port 4444"),
]


def normal_line():
    """Pick a normal (level, message) pair at random."""
    level = random.choices(list(LEVEL_WEIGHTS), weights=list(LEVEL_WEIGHTS.values()))[0]
    messages = [text for text, weight in NORMAL[level]]
    weights = [weight for text, weight in NORMAL[level]]
    message = random.choices(messages, weights=weights)[0]
    return level, message


def make_logs(count, with_problems, start):
    """Return a list of (time, level, message, kind) rows."""
    rows = []
    now = start

    while len(rows) < count:
        now += timedelta(seconds=random.randint(1, 10))  # time moves forward
        roll = random.random()                           # a number from 0.0 to 1.0

        if with_problems and roll < 0.004:
            # a single crash line
            rows.append((now, "CRITICAL", "System crash detected", "crash"))
        elif with_problems and roll < 0.008:
            # a message we have never seen before
            level, message = random.choice(RARE_MESSAGES)
            rows.append((now, level, message, "rare_message"))
        elif with_problems and roll < 0.012:
            # a burst: the same error again and again in a short time
            for _ in range(random.randint(5, 8)):
                now += timedelta(seconds=random.randint(1, 3))
                rows.append((now, "ERROR", "Request timeout while calling external service", "error_burst"))
        else:
            level, message = normal_line()
            rows.append((now, level, message, "normal"))

    return rows[:count]


def write_log(path, rows):
    """Write rows in the same format as the real logs."""
    with open(path, "w", encoding="utf-8") as f:
        for now, level, message, kind in rows:
            f.write(f"{now:%Y-%m-%d %H:%M:%S} [{level}] {message}\n")


def write_labels(path, rows):
    """Save one row per log line: line number, 1 if it is a problem, and its kind."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["line_number", "is_anomaly", "kind"])
        for number, row in enumerate(rows, start=1):
            kind = row[3]
            writer.writerow([number, int(kind != "normal"), kind])


if __name__ == "__main__":
    baseline = make_logs(3000, with_problems=False, start=datetime(2026, 10, 1, 10, 0, 0))
    test = make_logs(10000, with_problems=True, start=datetime(2026, 10, 2, 10, 0, 0))

    write_log("data/baseline.log", baseline)
    write_log("data/test.log", test)
    write_labels("data/test_labels.csv", test)

    problems = sum(1 for row in test if row[3] != "normal")
    print(f"baseline: {len(baseline)} lines, test: {len(test)} lines, {problems} are problems")
