"""Tests for UTC timestamp handling."""
from datetime import datetime, timezone

from src.utils.time_utils import utc_iso


class TestUtcIso:
    """Tests for the utc_iso helper function."""

    def test_utc_iso_produces_z_suffix(self):
        dt = datetime(2026, 3, 9, 16, 0, 0, tzinfo=timezone.utc)
        result = utc_iso(dt)
        assert result.endswith("Z"), f"Expected Z suffix, got: {result}"
        assert result == "2026-03-09T16:00:00Z"

    def test_utc_iso_with_microseconds(self):
        dt = datetime(2026, 3, 9, 16, 0, 0, 123456, tzinfo=timezone.utc)
        result = utc_iso(dt)
        assert result.endswith("Z")
        assert "123456" in result

    def test_utc_iso_none_returns_none(self):
        assert utc_iso(None) is None

    def test_utc_iso_no_plus_zero_offset(self):
        dt = datetime(2026, 3, 9, 16, 0, 0, tzinfo=timezone.utc)
        result = utc_iso(dt)
        assert "+00:00" not in result


class TestDatetimeNowUtc:
    """Verify datetime.now(timezone.utc) produces timezone-aware datetimes."""

    def test_now_utc_is_aware(self):
        now = datetime.now(timezone.utc)
        assert now.tzinfo is not None
        assert now.tzinfo == timezone.utc

    def test_now_utc_isoformat_has_offset(self):
        now = datetime.now(timezone.utc)
        iso = now.isoformat()
        assert "+00:00" in iso or iso.endswith("Z")

    def test_utc_iso_of_now_has_z(self):
        now = datetime.now(timezone.utc)
        result = utc_iso(now)
        assert result.endswith("Z")


class TestJavascriptCompatibility:
    """Verify the Z-suffixed strings work with JavaScript Date parsing rules."""

    def test_z_suffix_is_valid_iso8601(self):
        dt = datetime(2026, 3, 9, 16, 0, 0, tzinfo=timezone.utc)
        iso_z = utc_iso(dt)
        # Python can parse its own Z-suffixed output
        parsed = datetime.fromisoformat(iso_z.replace("Z", "+00:00"))
        assert parsed == dt

    def test_fromtimestamp_utc_is_aware(self):
        """Verify the pattern used for client_sent_msg_ts conversion."""
        epoch_ms = 1709971200000  # Some epoch timestamp in ms
        epoch_s = epoch_ms / 1000
        dt = datetime.fromtimestamp(epoch_s, tz=timezone.utc)
        assert dt.tzinfo == timezone.utc
