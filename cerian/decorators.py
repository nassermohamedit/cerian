import functools
from datetime import datetime, timedelta
from typing import Optional
from cerian.schedule import Periodic


def job(func):
    """Decorate a function that represent job."""
    @functools.wraps(func)
    def wrapper():
        func()
    wrapper.is_job = True
    return wrapper


def periodic(period: str | timedelta, start: Optional[datetime] = None, err: Optional[str | timedelta] = None):
    """Decorate job functions that must run in a periodic schedule."""
    def periodic_(func):
        def wrapper():
            func()
        wrapper.schedule = Periodic(period, start=start, err=err)
        return wrapper
    return periodic_
