from typing import TypeVar, Callable, Sequence, Optional

T = TypeVar("T")
Predicate = Callable[[T], bool]


def validate(value: T, checkers: Sequence[Predicate]) -> T:
    for checker in checkers:
        if not checker(value):
            raise ValueError
    return value


def validate_sequence(values: Sequence[T], predicates: Sequence[Predicate], msg: Optional[str] = None):
    if len(values) == 0:
        return values
    for v in values:
        for predicate in predicates:
            if not predicate(v):
                raise ValueError(f"{msg}: {v}" if msg is not None else str(v))
    return values