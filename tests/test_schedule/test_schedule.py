import pytest
from cerian.schedule import parse_timedelta_str
from datetime import timedelta


@pytest.mark.parametrize("period_str", ["3d:2h:30m:0ml", "3d:150m", "3d:30m:2h:0s", "74h:30m"])
def test_str_to_timedelta_success(period_str):
    assert parse_timedelta_str(period_str) == timedelta(days=3, hours=2, minutes=30)


@pytest.mark.parametrize("period_str", ["2H", "5", "2h:1h", "1d::3m", "1s:ml", ""])
def test_str_to_timedelta_fail(period_str):
    with pytest.raises(ValueError, match="Invalid period format"):
        parse_timedelta_str(period_str)

