import pytest
from src.schedule import Schedule
from datetime import timedelta


@pytest.mark.parametrize("period_str", ["3d2h30m", "3d150m", "3d30m2h0s", "74h30m"])
def test_src_to_timedelta_success(period_str):
    assert Schedule.str_to_timedelta(period_str) == timedelta(days=3, hours=2, minutes=30)


@pytest.mark.parametrize("period_str", ["2H", "5"])
def test_str_to_timedelta_fail(period_str):
    with pytest.raises(ValueError, match="invalid format"):
        Schedule.str_to_timedelta(period_str)
