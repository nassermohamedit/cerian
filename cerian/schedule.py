import abc
from datetime import timedelta, datetime
from abc import ABC


def parse_timedelta_str(period_str: str) -> timedelta:
    """
    Convert a string representation of a time period into a timedelta object.
    Format: "{days}d:{hours}h:{minutes}m:{seconds}s:{milliseconds}ml:{microseconds}mc".
    The order of components is not important, and each component must occur at most once
    """
    elements = {'mc': 0, 'ml': 0, 's': 0, 'm': 0, 'h': 0, 'd': 0}
    found = set()
    values = period_str.split(":")
    for e in values:
        try:
            if len(e) > 0 and e[-1] in elements:
                if e[-1] not in found:
                    elements[e[-1]] = int(e[:-1])
                    found.add(e[-1])
                else:
                    raise ValueError()
            elif len(e) > 1 and e[-2:] in elements:
                if e[-2:] not in found:
                    elements[e[-2:]] = int(e[:-2])
                    found.add(e[-2:])
                else:
                    raise ValueError()
            else:
                raise ValueError()
        except ValueError or TypeError:
            raise ValueError("Invalid period format")
    return timedelta(microseconds=elements['mc'], milliseconds=elements['ml'], seconds=elements['s'],
                     minutes=elements['m'], hours=elements['h'], days=elements['d'])


def validate_period(period: str | timedelta) -> timedelta:
    if isinstance(period, str):
        return parse_timedelta_str(period)
    if isinstance(period, timedelta):
        return period
    raise TypeError("period should be a string representation of a period or a timedelta object")


class TimeSequence(metaclass=abc.ABCMeta):
    """
    TimeSequence represents a finite or infinite sequence of time points over the time axis.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'tick') and callable(subclass.tick)
                and hasattr(subclass, "get_next_point") and callable(subclass.next_point))

    @abc.abstractmethod
    def tick(self) -> bool:
        """
        Returns whether the current time point (now) is in this sequence. Implementations must test if there is a
        time poit t in this sequence such that |now - t| < e.  e is a predefined time period,

        :return: True if and only if the above condition is satisfied.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def next_point(self):
        """
        Returns the next time point in this sequence relative to the current moment (now) or None if there is no next
        point.

        :return: datetime or None
        """
        raise NotImplementedError


class Periodic(TimeSequence):
    """
    A periodic sequence of time points.
    """
    def __init__(self, period: str | timedelta, start: datetime = None, max_delay: str | timedelta = None):
        self.period = validate_period(period)
        self.start = datetime.now() if start is None else start
        self.max_delay = timedelta(minutes=1) if max_delay is None else validate_period(max_delay)
        self.last_time = None

    def tick(self) -> bool:
        now = datetime.now()
        if now < self.start:
            return False
        if self.last_time is None:
            if now < self.start + self.max_delay:
                self.last_time = self.start
                return True
            self.last_time = self.start + ((now - self.start) // self.period) * self.period
            return self.tick()
        if self.period <= now - self.last_time <= self.period + self.max_delay:
            self.last_time += self.period
            return True
        if self.last_time < now:
            self.last_time += self.period * ((now - self.last_time) // self.period)
        return False

    def next_point(self) -> datetime:
        now = datetime.now()
        if now < self.start:
            return self.start
        last_time = self.start if self.last_time is None else self.last_time
        return last_time + self.period * ((now - last_time) // self.period + 1)


class Regular(TimeSequence):
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

    def tick(self):
        # TODO
        pass

    def next_point(self):
        # TODO
        pass
