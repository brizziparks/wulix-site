"""Date and time tools."""

from datetime import datetime
import locale


def get_datetime() -> str:
    """Return the current date and time."""
    now = datetime.now()
    return now.strftime("Le %A %d %B %Y à %H:%M:%S")
