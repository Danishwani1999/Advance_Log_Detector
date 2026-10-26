import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import detector  # noqa: E402


def test_error_rate_empty_window():
    assert detector.error_rate([]) == 0.0


def test_error_rate_share():
    assert detector.error_rate([True, False, False, False]) == 0.25


def test_word_boundary_ignores_embedded_words():
    assert detector.is_error("2026-10-19 12:00:01 [ERROR] Disk failure")
    assert not detector.is_error("2026-10-19 12:00:02 INFO terror alert cleared")


def test_window_forgets_old_lines():
    from collections import deque
    window = deque(maxlen=5)
    for _ in range(5):
        window.append(True)
    for _ in range(5):
        window.append(False)
    assert detector.error_rate(window) == 0.0
