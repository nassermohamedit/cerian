from cerian.decorators import job, periodic
from cerian.schedule import Periodic


def test_job_decorator():
    @job
    def task():
        print("I am a job to you?")

    assert task.__dict__.get("is_job", False)


def test_periodic_decorator():
    @periodic("1m")
    def periodic_task():
        print("I am periodic?")
    assert periodic_task.__dict__.get("period", None).period == Periodic(period="1m").period


