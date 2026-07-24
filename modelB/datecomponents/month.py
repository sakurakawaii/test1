from __future__ import annotations
from typing import Literal, cast, get_args
from calendar import monthrange
from datetime import datetime, timedelta
from .base import NamedNumericDateComponentBase
from .weekday import Weekday, WeekdayValue

type MonthName = Literal[
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

type MonthValue = MonthName | int

class Month(NamedNumericDateComponentBase[MonthName]):
    """Months of the year (1-based: 1 to 12)."""
    _NAMES = list(get_args(MonthName))
    _MIN = 1
    _MAX = 12

    _int_id: int
    _str_id: MonthName
    year: int | None = None

    def __init__(self, value: MonthValue, year: int | None = None):
        super().__init__(value)
        self.year = year

    def has_year(self) -> bool:
        return self.year is not None
    
    def year_or_default(self) -> int:
        """Returns the year if set, otherwise returns an arbitrary default (1970)."""
        return self.year if self.year is not None else 1970
    
    def monthrange(self) -> tuple[int, int]:
        """
        Wrapper around calendar.monthrange that accounts for the possibility of year being None.
        Requires year to be set for February to account for leap years.
        If year is None, uses 1970, as an arbitrary decision.
        """
        if self.int_id == 2 and self.has_year():
            raise ValueError("Year must be set to get length of February")
        
        return monthrange(self.year_or_default(), self.int_id)
    
    def nth_weekday(self, weekday: WeekdayValue | Weekday, n: int = 1) -> int:
        """
        Returns the day of the month corresponding to the nth occurrence of the given weekday in this month.
        For example, nth_weekday("monday", 2) would return the day of the month for the second Monday of this month.
        If n is less than 1, it will be treated as 1 (i.e. the first occurrence).
        Raises ValueError if n is greater than the number of occurrences of that weekday in this month.
        """
        if self.year is None:
            raise ValueError("Year must be set to calculate nth weekday")

        weekday = Weekday.create_from(weekday)

        if n < 1:
            n = 1
        
        weekday_int = weekday.int_id
        weekday_int_of_first = self.monthrange()[0]
        first_weekday = (7 - weekday_int_of_first + weekday_int) % 7 + 1
        nth_weekday = first_weekday + (n - 1) * 7

        if nth_weekday > len(self):
            raise ValueError(f"{n}th {weekday.str_id} does not exist in {self.str_id} of {self.year}.")

        return nth_weekday
        
    def last_nth_weekday(self, weekday: WeekdayValue | Weekday, n: int = 1) -> int:
        """
        Returns the day of the month corresponding to the nth occurrence of the given weekday from the end of this month.
        For example, last_nth_weekday("friday", 1) would return the day of the month for the last Friday of this month.
        If n is less than 1, it will be treated as 1 (i.e. the last occurrence).
        Raises ValueError if n is greater than the number of occurrences of that weekday in this month.
        """
        if self.year is None:
            raise ValueError("Year must be set to calculate last nth weekday")

        weekday = Weekday.create_from(weekday)

        if n < 1:
            n = 1
        
        # Shortcut - get the first weekday of the next month and use datetime to work backwards from there
        next_month = self + 1
        first_weekday_next_month = next_month.nth_weekday(weekday, 1)

        new_date = datetime(next_month.year_or_default(), next_month.int_id, first_weekday_next_month) - timedelta(weeks=n)

        if new_date.month != self.int_id:
            raise ValueError(f"Last {n}th {weekday.str_id} does not exist in {self.str_id} of {self.year}.")

        return new_date.day
    
    def _apply_loop(self, loop_count: int) -> Month:
        """
        Overrides the base _apply_loop to adjust the year when looping around the end or beginning of the month range.
        """
        if self.year is not None:
            self.year += loop_count
        return self
    
    def __eq__(self, other: object) -> bool:
        result = super().__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return result and self.year == cast(Month, other).year
    
    def __hash__(self) -> int:
        return hash((self.int_id, self.year))

    def __len__(self) -> int:
        """
        Get the length of the month in days. Requires year to be set for February to account for leap years.
        """
        return self.monthrange()[1]