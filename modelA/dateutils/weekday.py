from typing import Literal, cast, get_args
from .base import NamedNumericDateComponentBase

type WeekdayName = Literal[
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
]
type WeekdayValue = WeekdayName | int

class Weekday(NamedNumericDateComponentBase[WeekdayName]):
    """
    Days of the week (0-based: 0 to 6).
    Maintains parity with Python's datetime.date.weekday() where Monday is 0.
    """
    _NAMES = list(get_args(WeekdayName))
    _MIN = 0
    _MAX = 6