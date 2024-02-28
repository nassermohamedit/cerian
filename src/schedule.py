from abc import ABC
from datetime import timedelta, datetime


def str_to_timedelta(period_str: str):
    time_dict = {'s': 0, 'm': 0, 'h': 0, 'd': 0}
    num = "0"
    for c in period_str:
        if c in time_dict:
            time_dict[c] += int(num)
            num = "0"
        elif c.isdigit():
            num += c
        else:
            raise ValueError("invalid format")
    if num != "0":
        raise ValueError("invalid format")
    return timedelta(seconds=time_dict['s'], minutes=time_dict['m'], hours=time_dict['h'], days=time_dict['d'])


class Periodic:
    def __init__(self, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0,
                 start: datetime = None, max_delay=None):
        self.start = datetime.now() if start is None else start
        self.period = None
        if seconds != 0 or minutes != 0 or hours != 0 or days != 0:
            self.period = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        self.last_time = None
        self.max_delay = timedelta(minutes=1) if max_delay is None else max_delay

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


class Regular:
    def __init__(self, minutes, hours, week_days, month_days, start, max_delay):
        if all([0 <= m <= 59 for m in minutes]):
            self.minutes = sorted(minutes)
        else:
            raise Exception("minutes must be >= 0 and < 59")

        if all([0 <= h <= 23 for h in hours]):
            self.hours = sorted(hours)
        else:
            raise Exception("hours must be >= 0 and < 24")

        if all([0 <= d <= 6 for d in week_days]):
            self.wdays = sorted(week_days)
        else:
            raise Exception("week days must be >= 0 and < 6")

        if all([1 <= h <= 31 for h in month_days]):
            self.mdays = sorted(month_days)
        else:
            raise Exception("month days must be >= 1 and < 31")

        self.start = datetime.now() if start is None else start
        self.last_time = None
        self.max_delay = max_delay

    def tik(self):
        # TODO
        pass
