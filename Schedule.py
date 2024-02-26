from abc import ABC
from datetime import timedelta, datetime


class Schedule(ABC):
    def get_next_time(self):
        raise NotImplementedError()


class Periodic(Schedule):
    def __init__(self, minutes: int = 0, hours: int = 0, days: int = 0, start: datetime = None):
        self.start = datetime.now().replace(second=0, microsecond=0) if start is None else start.replace(second=0, microsecond=0)
        self.period = None
        if minutes != 0 or hours != 0 or days != 0:
            self.period = timedelta(minutes=minutes, hours=hours, days=days)

    def get_next_time(self):
        generations = self.no_generations()
        return self.start + self.period * generations

    def no_generations(self):
        now = datetime.now().replace(microsecond=0, second=0)
        return (now - self.start) // self.period + 1

