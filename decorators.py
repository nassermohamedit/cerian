import functools


def job(minutes, hours, days):
    def job_(func):
        @functools.wraps(func)
        def wrapper():
            func()
        wrapper.__schedule__ = (minutes, hours, days)
        wrapper.__decorator_name__ = "job"
        return wrapper
    return job_


@job(0, 0, 1)
def tasky():
    print("watachiwayanokaaaa")