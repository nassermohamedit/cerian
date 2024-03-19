import time
import pytest
from datetime import datetime, timedelta
from cerian.schedule import Periodic, validate_period


def test_periodic_constructor_with_str_period():
    period = "1h:30m"
    instance = Periodic(period)
    assert instance.period == timedelta(hours=1, minutes=30)


def test_periodic_constructor_with_timedelta_period():
    period = timedelta(hours=1, minutes=30)
    instance = Periodic(period)
    assert instance.period == timedelta(hours=1, minutes=30)


def test_periodic_constructor_with_invalid_value():
    period = 10
    with pytest.raises(TypeError, match="period should be a string representation of a period or a timedelta object"):
        Periodic(period)


def test_periodic_constructor_with_default_err():
    instance = Periodic("1h")
    assert instance.err == timedelta(seconds=1)


def test_periodic_constructor_with_err():
    instance = Periodic("1h", err="1m")
    assert instance.err == timedelta(minutes=1)


def test_periodic_constructor_with_start():
    now = datetime.now()
    instance = Periodic("1h", start=now)
    assert instance.start == now


def test_periodic_in():
    t = datetime.now()
    seq = Periodic("1h", start=t)
    period = validate_period("1h") // 2
    expected = True
    for i in range(10):
        assert (t in seq) == expected
        expected = not expected
        t += period


@pytest.mark.nonrepeatable
@pytest.mark.slow
def test_periodic_tick():
    periodic = Periodic("60s", err="5s")
    expected = True
    for i in range(10):
        assert periodic.tick() is expected
        expected = not expected
        if not expected:
            assert periodic.tick() is expected
        time.sleep(30)


def test_periodic_tick_before_start():
    start = datetime.now() + timedelta(seconds=10)
    periodic = Periodic("1m", start=start)
    assert periodic.tick() is False


def test_get_next_time_before_start():
    start = datetime.now() + timedelta(minutes=1)
    periodic = Periodic("1s", start=start)
    assert periodic.next_point() == start


def test_get_next_time_after_start():
    start = datetime.now().replace(microsecond=0, second=0)
    periodic = Periodic("1m", start=start)
    assert periodic.next_point() == start + timedelta(minutes=1)
