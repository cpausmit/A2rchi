from datetime import datetime, timezone


def utc_iso(dt: datetime) -> str:
    """Convert a UTC-aware datetime to an ISO 8601 string with Z suffix."""
    if dt is None:
        return None
    return dt.isoformat().replace('+00:00', 'Z')
