"""Turn a log message into a 'template' by hiding the parts that keep changing."""
import re


def to_template(message):
    """'Disk usage above 75 percent' -> 'Disk usage above <NUM> percent'."""
    return re.sub(r"\d+", "<NUM>", message)
