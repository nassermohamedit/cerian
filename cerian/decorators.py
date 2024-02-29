import functools
from datetime import datetime, timedelta
from schedule import Periodic


def job(func):
    @functools.wraps(func)
    def wrapper():
        func()
    wrapper.is_job = True
    return wrapper


def periodic(period: str | timedelta, start: datetime = None, max_delay: str | timedelta = None):
    def periodic_(func):
        def wrapper():
            func()
        wrapper.period = Periodic(period, start=start, max_delay=max_delay)
        return wrapper
    return periodic_

