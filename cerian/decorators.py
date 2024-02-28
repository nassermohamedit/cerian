import functools
from datetime import timedelta
from cerian.schedule import Periodic


def job(func):
    @functools.wraps(func)
    def wrapper():
        func()
    wrapper.is_job = True
    return wrapper


def periodic(period: str | timedelta):
    def periodic_(func):
        def wrapper():
            func()
        wrapper.period = Periodic(period)
        return wrapper
    return periodic_


if __name__ == "__main__":
    pass
