from detector import is_error


def test_error_line_detected():
    assert is_error("2026-10-14 10:00:00 [ERROR] Database down")


def test_critical_line_detected():
    assert is_error("2026-10-14 10:00:00 [CRITICAL] Out of memory")


def test_info_line_ignored():
    assert not is_error("2026-10-14 10:00:00 [INFO] Health check passed")
