def parse_log_line(line: str) -> str:
    """Extracts log level from a standard log line."""
    line_upper = line.upper()
    if "ERROR" in line_upper:
        return "ERROR"
    elif "WARN" in line_upper or "WARNING" in line_upper:
        return "WARNING"
    elif "INFO" in line_upper:
        return "INFO"
    return "UNKNOWN"
