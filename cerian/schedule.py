import abc
from datetime import timedelta, datetime
from typing import Optional, override, Sequence


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
        except (ValueError, TypeError):
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

    MINUTES = [i for i in range(0, 60)]
    HOURS = [i for i in range(0, 24)]
    DAYS = [i for i in range(32)]
    WEEK_DAYS = [i for i in range(0, 7)]
    MONTHS = [i for i in range(1, 13)]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'tick') and callable(subclass.tick)
                and hasattr(subclass, "next_point") and callable(subclass.next_point))

    @abc.abstractmethod
    def tick(self) -> bool:
        """
        Returns whether the current time point (now) is in this sequence. Implementations must test if there is a
        time poit t in this sequence such that |now - t| < e.  e is a predefined time period,

        :return: True if and only if the above condition is satisfied.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, item: datetime):
        """
        Returns whether the provided time point is in this sequence.
        """
        raise NotImplementedError


class Periodic(TimeSequence):
    """
    A periodic sequence of time points.
    """

    def __init__(self,
                 period: str | timedelta,
                 start: Optional[datetime] = None,
                 err: Optional[str | timedelta] = None):
        self.period = validate_period(period)
        self.start = start or datetime.now()
        self.err = timedelta(seconds=1) if err is None else validate_period(err)
        self._last_time = None

    @override
    def tick(self):
        now = datetime.now()
        if self._last_time is not None and abs(now - self._last_time) < self.err:
            return False
        if self._last_time is None:
            if abs(now - self.start) < self.err:
                self._last_time = self.start
                return True
            if now < self.start:
                return False
        tp = self.start + ((now - self.start) // self.period) * self.period
        if abs(tp - now) < self.err:
            self._last_time = tp
            return True
        tp += self.period
        if abs(tp - now) < self.err:
            self._last_time = tp
            return True
        return False

    @override
    def next_point(self):
        """
        Returns the next time point in this sequence relative to the current moment (now) or None if there is no next
        point.

        :return: datetime or None
        """
        now = datetime.now()
        if now < self.start:
            return self.start
        tp = self.start + ((now - self.start) // self.period) * self.period
        return tp + self.period

    @override
    def __contains__(self, item):
        if abs(item - self.start) < self.err:
            return True
        if item < self.start:
            return False
        tp = self.start + ((item - self.start) // self.period) * self.period
        if abs(tp - item) < self.err or abs(tp + self.period - item) < self.err:
            return True
        return False
