import functools
from schedule import Periodic


def job(minutes=0, hours=0, days=0, start_time=None, max_delay=None):
    def job_(func):
        @functools.wraps(func)
        def wrapper():
            func()
        wrapper.schedule = Periodic(minutes=minutes, hours=hours, days=days, max_delay=max_delay, start=start_time)
        wrapper.__decorator_name__ = "job"
        return wrapper
    return job_


@job(0, 0, 1)
def tasky():
    print("watachiwayanokaaaa")