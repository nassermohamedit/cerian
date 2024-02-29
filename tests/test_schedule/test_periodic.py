import time
import pytest
from datetime import datetime, timedelta
from cerian.schedule import Periodic


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


def test_periodic_constructor_with_default_max_delay():
    instance = Periodic("1h")
    assert instance.max_delay == timedelta(minutes=1)


def test_periodic_constructor_with_max_delay():
    instance = Periodic("1h", max_delay="1m")
    assert instance.max_delay == timedelta(minutes=1)


def test_periodic_constructor_with_start():
    now = datetime.now()
    instance = Periodic("1h", start=now)
    assert instance.start == now


@pytest.mark.nonrepeatable
@pytest.mark.slow
def test_periodic_tik():
    periodic = Periodic("500ml", max_delay="10ml")
    expected = True
    for i in range(10):
        assert periodic.tick() is expected
        expected = not expected
        time.sleep(0.25)


def test_periodic_tik_before_start():
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
