from __future__ import annotations
from dataclasses import dataclass, astuple
from datetime import timedelta
import math

@dataclass(frozen=True, eq=False)
class Duration:
    seconds: float = 0
    minutes: float = 0
    hours: float = 0
    days: float = 0
    months: float = 0
    years: float = 0

    # Specified after the other units just for dev experience
    weeks: float = 0
    weekdays: float = 0

    # Optionally specify exact lengths of months and years in days
    # instead of varying based on the current date.
    month_days: float | None = None
    year_days: float | None = None

    @classmethod
    def from_seconds(cls, seconds: int | float) -> Duration:
        return cls(seconds=seconds)

    @classmethod
    def from_timedelta(cls, td: timedelta) -> Duration:
        return cls(days=td.days, seconds=td.seconds + td.microseconds / 1_000_000)

    @classmethod
    def create_from(cls, value: Duration | timedelta | int | float) -> Duration:
        if isinstance(value, Duration):
            return value
        if isinstance(value, timedelta):
            return cls.from_timedelta(value)
        if isinstance(value, (int, float)):
            return cls.from_seconds(value)
        raise TypeError(f"Cannot create Duration from {type(value).__name__}")

    def to_timedelta(self) -> timedelta:
        return timedelta(seconds=self.total_seconds())
    
    def total_seconds(self) -> float:
        s = self.simplify()
        s._assert_exact()
        return (
            s.seconds
            + s.minutes * 60
            + s.hours * 3600
            + s.days * 8640
            + s.weeks * 604800
        )
    
    def _assert_exact(self) -> None:
        s = self.simplify()
        if s.weekdays != 0:
            raise ValueError("Duration has weekdays, which have no fixed length")
        if s.months != 0:
            raise ValueError("Duration has months but month_days is not set")
        if s.years != 0:
            raise ValueError("Duration has years but year_days is not set")
        
    def is_simplified(self) -> bool:
        return astuple(self) == astuple(self.simplify())

    def simplify(self) -> Duration:
        try:
            return object.__getattribute__(self, '_simplified_cache')
        except AttributeError:
            pass

        total_seconds: float = self.seconds
        total_minutes: float = self.minutes
        total_hours: float = self.hours
        total_days: float = self.days + self.weeks * 7
        months = self.months
        years = self.years

        if self.year_days is not None:
            total_days += years * self.year_days
            years = 0

        if self.month_days is not None:
            total_days += months * self.month_days
            months = 0

        # Cascade fractional days down to smaller units
        # math.floor is used instead of int() so negatives are handled correctly
        total_days_floor = math.floor(total_days)
        total_hours += (total_days - total_days_floor) * 24
        total_days = total_days_floor

        total_hours_floor = math.floor(total_hours)
        total_minutes += (total_hours - total_hours_floor) * 60
        total_hours = total_hours_floor

        total_minutes_floor = math.floor(total_minutes)
        total_seconds += (total_minutes - total_minutes_floor) * 60
        total_minutes = total_minutes_floor

        # Normalize upward: seconds → minutes → hours → days → weeks
        total_minutes += int(total_seconds) // 60
        total_seconds = total_seconds % 60

        total_hours += total_minutes // 60
        total_minutes = total_minutes % 60

        total_days += total_hours // 24
        total_hours = total_hours % 24

        total_weeks = total_days // 7
        total_days = total_days % 7

        result = Duration(
            seconds=total_seconds,
            minutes=total_minutes,
            hours=total_hours,
            days=total_days,
            months=months,
            years=years,
            weekdays=self.weekdays,
            weeks=total_weeks,
            year_days=self.year_days,
            month_days=self.month_days,
        )
        object.__setattr__(self, '_simplified_cache', result)
        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        # Fast path: identical fields
        if astuple(self) == astuple(other):
            return True
        # Slow path: compare simplified forms via direct tuple comparison (avoids recursion)
        return astuple(self.simplify()) == astuple(other.simplify())

    def __hash__(self) -> int:
        return hash(astuple(self.simplify()))

    def __add__(self, other: Duration | timedelta | int | float) -> Duration:
        if not isinstance(other, (Duration, timedelta, int, float)):
            return NotImplemented
        other = Duration.create_from(other)
        a = self.simplify()
        b = other.simplify()

        # After simplification, years/months are already folded into days when
        # year_days/month_days are set, so conflicting exact lengths can't affect the sum.
        year_days = a.year_days if a.year_days is not None else b.year_days
        month_days = a.month_days if a.month_days is not None else b.month_days
        return Duration(
            seconds=a.seconds + b.seconds,
            minutes=a.minutes + b.minutes,
            hours=a.hours + b.hours,
            days=a.days + b.days,
            months=a.months + b.months,
            years=a.years + b.years,
            weeks=a.weeks + b.weeks,
            weekdays=a.weekdays + b.weekdays,
            year_days=year_days,
            month_days=month_days,
        ).simplify()

    def __radd__(self, other: timedelta | int | float) -> Duration:
        if not isinstance(other, (timedelta, int, float)):
            return NotImplemented
        return Duration.create_from(other) + self

    def __sub__(self, other: Duration | timedelta | int | float) -> Duration:
        if not isinstance(other, (Duration, timedelta, int, float)):
            return NotImplemented
        return self + (-Duration.create_from(other))

    def __rsub__(self, other: timedelta | int | float) -> Duration:
        if not isinstance(other, (timedelta, int, float)):
            return NotImplemented
        return Duration.create_from(other) - self

    def __neg__(self) -> Duration:
        return Duration.create_from(-self.total_seconds())

    def __mul__(self, other: int | float) -> Duration:
        if not isinstance(other, (int, float)):
            return NotImplemented
        s = self.simplify()
        s._assert_exact()
        return Duration(
            seconds=s.seconds * other,
            minutes=s.minutes * other,
            hours=s.hours * other,
            days=s.days * other,
            weeks=s.weeks * other,
            weekdays=s.weekdays * other,
            months=s.months * other,
            years=s.years * other,
            year_days=s.year_days,
            month_days=s.month_days,
        ).simplify()

    def __rmul__(self, other: int | float) -> Duration:
        return self.__mul__(other)

    def __truediv__(self, other: Duration | timedelta | int | float) -> Duration | float:
        if isinstance(other, (int, float)):
            s = self.simplify()
            s._assert_exact()
            return Duration(
                seconds=s.seconds / other,
                minutes=s.minutes / other,
                hours=s.hours / other,
                days=s.days / other,
                weeks=s.weeks / other,
                year_days=s.year_days,
                month_days=s.month_days,
            ).simplify()
        if isinstance(other, (Duration, timedelta)):
            return self.total_seconds() / Duration.create_from(other).total_seconds()
        return NotImplemented

    def __abs__(self) -> Duration:
        if self.total_seconds() < 0:
            return -self
        return self

    def __bool__(self) -> bool:
        return self.total_seconds() != 0

    def __pos__(self) -> Duration:
        return self

    def __lt__(self, other: Duration | timedelta | int | float) -> bool:
        if not isinstance(other, (Duration, timedelta, int, float)):
            return NotImplemented
        return self.total_seconds() < Duration.create_from(other).total_seconds()

    def __le__(self, other: Duration | timedelta | int | float) -> bool:
        if not isinstance(other, (Duration, timedelta, int, float)):
            return NotImplemented
        return self.total_seconds() <= Duration.create_from(other).total_seconds()

    def __gt__(self, other: Duration | timedelta | int | float) -> bool:
        if not isinstance(other, (Duration, timedelta, int, float)):
            return NotImplemented
        return self.total_seconds() > Duration.create_from(other).total_seconds()

    def __ge__(self, other: Duration | timedelta | int | float) -> bool:
        if not isinstance(other, (Duration, timedelta, int, float)):
            return NotImplemented
        return self.total_seconds() >= Duration.create_from(other).total_seconds()

