from __future__ import annotations
from typing import Literal, cast, get_args
from .base import NamedNumericDateComponentBase

type SeasonName = Literal["spring", "summer", "autumn", "winter", "fall"]
type SeasonValue = SeasonName | int

class Season(NamedNumericDateComponentBase[SeasonName]):
    """Meteorological seasons (1-based: 1 to 4)."""
    _NAMES = list(get_args(SeasonName))
    _MIN = 1
    _MAX = 4
    _ALIASES = {"fall": "autumn"}

    year: int | None = None

    def __init__(self, value: SeasonValue, year: int | None = None):
        super().__init__(value)
        self.year = year

    def has_year(self) -> bool:
        return self.year is not None
    
    def year_or_default(self) -> int:
        """Returns the year if set, otherwise returns an arbitrary default (1970)."""
        return self.year if self.year is not None else 1970
    
    def _apply_loop(self, loop_count: int) -> Season:
        """
        Overrides the base _apply_loop to adjust the year when looping around the end or beginning of the season range.
        """
        if self.year is not None:
            self.year += loop_count
        return self
    
    def __eq__(self, other: object) -> bool:
        result = super().__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return result and self.year == cast(Season, other).year
    
    def __hash__(self) -> int:
        return hash((self.int_id, self.year))
