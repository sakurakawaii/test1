"""Tests for dateutils/weekday.py (run against the corrected FixedWeekday
subclass; the shipped class cannot be instantiated - see REPORT.md D1).

TestWeekday inherits the whole numeric contract from TestMinute and *negates*
`rejects_string_values`, since named components override normalization to
accept name strings - demonstrating the override was implemented correctly.
"""
import pytest
from abc import ABC
from datetime import date
from typing import Any

from test_utils import Mixin
from test_minute import TestMinute
from dateutils.base import NumericDateComponentBase, NamedNumericDateComponentBase
from mixins_named import NamedComponentMixins
from helpers import FixedWeekday


class MatchesDatetimeWeekdayOrderMixinBase(Mixin, ABC):
    """Feature: Weekday numbering matches datetime.date.weekday() (Monday=0)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "matches_datetime_weekday_order":
            # 2024-01-01 was a Monday; 2024-01-06 a Saturday.
            return (
                FixedWeekday("monday").int_id == date(2024, 1, 1).weekday()
                and FixedWeekday("saturday").int_id == date(2024, 1, 6).weekday()
            )
        return super().condition(feature, *args, **kwargs)


class MatchesDatetimeWeekdayOrderMixin(MatchesDatetimeWeekdayOrderMixinBase, ABC):
    negative_matches_datetime_weekday_order: bool = False

    @pytest.mark.feature_datetime_parity
    def test_matches_datetime_weekday_order(self) -> None:
        """Weekday ints line up with the stdlib's Monday=0 convention."""
        assert self.validate("matches_datetime_weekday_order")


class NoMatchesDatetimeWeekdayOrderMixin(MatchesDatetimeWeekdayOrderMixinBase, ABC):
    negative_matches_datetime_weekday_order: bool = True

    @pytest.mark.feature_datetime_parity
    def test_matches_datetime_weekday_order(self) -> None:
        """Negated variant: numbering must not match the stdlib."""
        assert self.validate("matches_datetime_weekday_order")


class TestWeekday(TestMinute, NamedComponentMixins, MatchesDatetimeWeekdayOrderMixin):
    """Weekday = numeric contract (strings now accepted) + naming contract."""

    # Named components *accept* strings: the inherited rejection test flips.
    negative_rejects_string_values: bool = True

    @pytest.fixture
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]:
        return FixedWeekday

    @pytest.fixture
    def min_value(self) -> int:
        return 0

    @pytest.fixture
    def max_value(self) -> int:
        return 6

    @pytest.fixture
    def in_range_value(self) -> int:
        return 2

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 5

    @pytest.fixture
    def safe_delta(self) -> int:
        # 2 +/- 2 stays inside 0..6.
        return 2

    @pytest.fixture
    def sample_name(self) -> str:
        return "wednesday"

    @pytest.fixture
    def sample_name_int(self) -> int:
        return 2

    @pytest.fixture
    def other_name(self) -> str:
        return "saturday"

    @pytest.fixture
    def other_name_int(self) -> int:
        return 5
