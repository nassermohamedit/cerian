import time
from abc import ABC
from datetime import timedelta, datetime
import multiprocessing


class Schedule(ABC):

    def tik(self) -> bool:
        raise NotImplementedError()


class Periodic(Schedule):
    def __init__(self, max_delay, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0,
                 start: datetime = None):
        self.start = datetime.now() if start is None else start
        self.period = None
        if seconds != 0 or minutes != 0 or hours != 0 or days != 0:
            self.period = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        self.last_time = None
        self.max_delay = max_delay

    def tik(self) -> bool:
        now = datetime.now()
        if now < self.start:
            return False
        if self.last_time is None:
            if now < self.start + self.max_delay:
                self.last_time = self.start
                return True
            self.last_time = self.start + ((now - self.start) // self.period) * self.period
            return self.tik()
        if self.period <= now - self.last_time <= self.period + self.max_delay:
            self.last_time += self.period
            return True
        if self.last_time < now:
            self.last_time += self.period * ((now - self.last_time) // self.period)
        return False
