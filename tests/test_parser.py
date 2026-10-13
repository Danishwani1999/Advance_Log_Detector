import pytest
from src.logdetector.parser import parse_log_line

def test_parse_error_log():
    line = "2026-10-13 10:00:00 [ERROR] Database connection failed"
    assert parse_log_line(line) == "ERROR"

def test_parse_warning_log():
    line = "2026-10-13 10:01:00 [WARNING] Disk space running low"
    assert parse_log_line(line) == "WARNING"

def test_parse_info_log():
    line = "2026-10-13 10:02:00 [INFO] Service started successfully"
    assert parse_log_line(line) == "INFO"

def test_parse_unknown_log():
    line = "2026-10-13 10:03:00 [DEBUG] Detailed diagnostic trace"
    assert parse_log_line(line) == "UNKNOWN"

def test_parse_lowercase_log():
    line = "error: fatal exception occurred"
    assert parse_log_line(line) == "ERROR"
