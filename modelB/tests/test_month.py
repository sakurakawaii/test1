"""
Tests for datecomponents/month.py.

The shipped Month has an empty _NAMES list on Python 3.12+ (defect D1, see
REPORT.md and tests/test_rejections.py). `UsableMonth` follows the documented
extension contract to supply the intended names so Month's own calendar logic
can be verified.

Known defects keep parts of Month out of the standard suite (all verified in
tests/test_rejections.py instead):
 * D2 - wrap-around `+`/`-` and year carrying are broken.
 * D3 - `monthrange()` has an inverted February condition.
 * D1 - `nth_weekday`/`last_nth_weekday` construct the broken `Weekday`
   internally, so only their no-year guard clauses are reachable.
"""
from abc import ABC
from typing import Any

import pytest

from datecomponents.minute import Minute
from datecomponents.month import Month
from tests.mixins.named import NamedComponentMixin
from tests.mixins.numeric import ComponentFixturesMixin, PlainNumericComponentMixin
from tests.mixins.yeared import (
    HasYearMixin,
    NoEqualWithDifferentYearMixin,
    NoYearDefaultIs1970Mixin,
    YearOrDefaultReturnsOwnYearMixin,
)
from tests.test_utils import Mixin

MONTH_NAMES = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]


class UsableMonth(Month):
    """Month with the names its `MonthName` alias declares (D1 workaround)."""

    _NAMES = MONTH_NAMES


# --- feature: monthrange_reports_weekday_and_length (Month-specific) -----------

class MonthrangeReportsWeekdayAndLengthMixinBase(Mixin, ABC):
    """monthrange() returns (first weekday, number of days) for the month."""

    @pytest.fixture
    def calendar_month(self) -> Month:
        """A non-February month (February is defective - D3)."""
        raise NotImplementedError

    @pytest.fixture
    def expected_monthrange(self) -> tuple[int, int]:
        """The (first weekday, day count) expected for `calendar_month`."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "monthrange_reports_weekday_and_length":
            calendar_month: Month = kwargs["calendar_month"]
            expected: tuple[int, int] = kwargs["expected_monthrange"]
            return calendar_month.monthrange() == expected
        return super().condition(feature, *args, **kwargs)


class MonthrangeReportsWeekdayAndLengthMixin(
    MonthrangeReportsWeekdayAndLengthMixinBase, ABC
):
    negative_monthrange_reports_weekday_and_length: bool = False

    @pytest.mark.calendar
    def test_monthrange_reports_weekday_and_length(
        self, calendar_month: Month, expected_monthrange: tuple[int, int]
    ) -> None:
        """monthrange() mirrors calendar.monthrange for the stored/default year."""
        assert self.validate(
            "monthrange_reports_weekday_and_length",
            calendar_month=calendar_month,
            expected_monthrange=expected_monthrange,
        )


class NoMonthrangeReportsWeekdayAndLengthMixin(
    MonthrangeReportsWeekdayAndLengthMixin, ABC
):
    negative_monthrange_reports_weekday_and_length: bool = True


# --- feature: len_counts_days (Month-specific) -----------------------------------

class LenCountsDaysMixinBase(MonthrangeReportsWeekdayAndLengthMixinBase, ABC):
    """len(month) is the day count - the second monthrange element."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "len_counts_days":
            calendar_month: Month = kwargs["calendar_month"]
            expected: tuple[int, int] = kwargs["expected_monthrange"]
            return len(calendar_month) == expected[1]
        return super().condition(feature, *args, **kwargs)


class LenCountsDaysMixin(LenCountsDaysMixinBase, ABC):
    negative_len_counts_days: bool = False

    @pytest.mark.calendar
    def test_len_counts_days(
        self, calendar_month: Month, expected_monthrange: tuple[int, int]
    ) -> None:
        """len() reports the number of days in the month."""
        assert self.validate(
            "len_counts_days",
            calendar_month=calendar_month,
            expected_monthrange=expected_monthrange,
        )


class NoLenCountsDaysMixin(LenCountsDaysMixin, ABC):
    negative_len_counts_days: bool = True


# --- feature: fails_nth_weekday_without_year (Month-specific) ---------------------

class FailsNthWeekdayWithoutYearMixinBase(Mixin, ABC):
    """Both nth_weekday and last_nth_weekday demand a year up front."""

    fail_fails_nth_weekday_without_year: type[BaseException] = ValueError

    @pytest.fixture
    def yearless_month(self) -> Month:
        """A month constructed without a year."""
        raise NotImplementedError

    @pytest.fixture
    def nth_weekday_method(self) -> str:
        """Which method to call: 'nth_weekday' or 'last_nth_weekday'."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_nth_weekday_without_year":
            yearless_month: Month = kwargs["yearless_month"]
            method: str = kwargs["nth_weekday_method"]
            # The guard clause fires before the weekday argument is inspected,
            # so the (defective, D1) Weekday class is never constructed here.
            getattr(yearless_month, method)("monday")
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsNthWeekdayWithoutYearMixin(FailsNthWeekdayWithoutYearMixinBase, ABC):
    negative_fails_nth_weekday_without_year: bool = False

    @pytest.mark.calendar
    def test_fails_nth_weekday_without_year(
        self, yearless_month: Month, nth_weekday_method: str
    ) -> None:
        """nth_weekday raises ValueError when no year is available."""
        self.validate(
            "fails_nth_weekday_without_year",
            yearless_month=yearless_month,
            nth_weekday_method="nth_weekday",
        )

    @pytest.mark.calendar
    def test_fails_last_nth_weekday_without_year(
        self, yearless_month: Month, nth_weekday_method: str
    ) -> None:
        """last_nth_weekday raises ValueError when no year is available."""
        self.validate(
            "fails_nth_weekday_without_year",
            yearless_month=yearless_month,
            nth_weekday_method="last_nth_weekday",
        )


class NoFailsNthWeekdayWithoutYearMixin(FailsNthWeekdayWithoutYearMixin, ABC):
    negative_fails_nth_weekday_without_year: bool = True


class TestMonth(PlainNumericComponentMixin, NamedComponentMixin):
    """Month's inherited numeric/named behavior (year-independent)."""

    @pytest.fixture
    def component_cls(self) -> type[UsableMonth]:
        return UsableMonth

    @pytest.fixture
    def valid_int(self) -> int:
        # 5 = may (1-based).
        return 5

    @pytest.fixture
    def valid_name(self) -> str:
        return "may"

    @pytest.fixture
    def add_delta(self) -> int:
        # 5 + 6 = 11 < 12: strictly below _MAX (wrap-around is defective, D2).
        return 6

    @pytest.fixture
    def sub_delta(self) -> int:
        # 5 - 4 = 1 == _MIN: landing on _MIN does not wrap.
        return 4

    @pytest.fixture
    def other_typed_value(self) -> Minute:
        return Minute(5)


class TestMonthWithYear(
    HasYearMixin,
    YearOrDefaultReturnsOwnYearMixin,
    NoYearDefaultIs1970Mixin,
    NoEqualWithDifferentYearMixin,
    MonthrangeReportsWeekdayAndLengthMixin,
    LenCountsDaysMixin,
):
    """Year-aware Month behavior with a year supplied."""

    @pytest.fixture
    def yeared_subject(self) -> UsableMonth:
        return UsableMonth("may", 2024)

    @pytest.fixture
    def expected_year(self) -> int:
        return 2024

    @pytest.fixture
    def different_year_subject(self) -> UsableMonth:
        return UsableMonth("may", 2025)

    @pytest.fixture
    def calendar_month(self) -> UsableMonth:
        return UsableMonth("march", 2024)

    @pytest.fixture
    def expected_monthrange(self) -> tuple[int, int]:
        # March 1st 2024 was a Friday (4); March has 31 days.
        return (4, 31)


class TestMonthWithoutYear(TestMonthWithYear, FailsNthWeekdayWithoutYearMixin):
    """
    Year-less Month behavior: inherits every test from TestMonthWithYear and
    flips the `negative_*` flags for the features the missing year overrides.
    """

    # No year -> has_year() is now False.
    negative_has_year: bool = True
    # No year -> year_or_default() no longer echoes `expected_year`.
    negative_year_or_default_returns_own_year: bool = True
    # ...because it falls back to 1970 instead (un-negating the parent's No mixin).
    negative_year_default_is_1970: bool = False

    @pytest.fixture
    def yeared_subject(self) -> UsableMonth:
        return UsableMonth("may")

    @pytest.fixture
    def calendar_month(self) -> UsableMonth:
        return UsableMonth("march")

    @pytest.fixture
    def expected_monthrange(self) -> tuple[int, int]:
        # Falls back to 1970: March 1st 1970 was a Sunday (6); 31 days.
        return (6, 31)

    @pytest.fixture
    def yearless_month(self) -> UsableMonth:
        return UsableMonth("june")

    @pytest.fixture
    def nth_weekday_method(self) -> str:
        return "nth_weekday"
