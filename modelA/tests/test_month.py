"""Tests for dateutils/month.py (via the corrected FixedMonth; REPORT.md D1).

February-specific behavior and wrap-around year handling are defective
(REPORT.md D3/D4/D5) and are exercised only in test_reject_verification.py.
`nth_weekday` internally uses the *shipped* Weekday class, which is broken
(D1), so those features patch Weekday's name table via pytest-mock - the
minimum intervention needed to reach the otherwise-real logic.
"""
import pytest
from abc import ABC, abstractmethod
from calendar import monthrange
from typing import Any
from pytest_mock import MockerFixture

from test_utils import Mixin
from dateutils.base import NamedNumericDateComponentBase
from dateutils.weekday import Weekday
from mixins_numeric import PlainNumericComponentMixins
from mixins_named import NamedComponentMixins, YearedComponentMixins
from helpers import FixedMonth, WEEKDAY_NAMES


class ComputesMonthrangeMixinBase(Mixin, ABC):
    """Feature: monthrange() mirrors calendar.monthrange for non-February
    months, defaulting the year to 1970 when unset."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "computes_monthrange":
            return (
                FixedMonth(5, 2024).monthrange() == monthrange(2024, 5)
                and FixedMonth(5).monthrange() == monthrange(1970, 5)
                # length comes from the same computation via __len__
                and len(FixedMonth(1, 2021)) == 31
                and len(FixedMonth(4)) == 30
            )
        return super().condition(feature, *args, **kwargs)


class ComputesMonthrangeMixin(ComputesMonthrangeMixinBase, ABC):
    negative_computes_monthrange: bool = False

    @pytest.mark.feature_calendar_math
    def test_computes_monthrange(self) -> None:
        """monthrange()/len() follow the stdlib calendar for non-Feb months."""
        assert self.validate("computes_monthrange")


class NoComputesMonthrangeMixin(ComputesMonthrangeMixinBase, ABC):
    negative_computes_monthrange: bool = True

    @pytest.mark.feature_calendar_math
    def test_computes_monthrange(self) -> None:
        """Negated variant: monthrange must not match the stdlib."""
        assert self.validate("computes_monthrange")


class FindsNthWeekdayMixinBase(Mixin, ABC):
    """Feature: nth_weekday finds the nth given weekday of the month."""

    @pytest.fixture
    @abstractmethod
    def working_weekday(self) -> None:
        """Setup fixture restoring Weekday's name table (broken per D1)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "finds_nth_weekday":
            may = FixedMonth(5, 2024)  # May 2024 starts on a Wednesday
            return (
                may.nth_weekday("wednesday") == 1
                and may.nth_weekday("monday", 2) == 13
                and may.nth_weekday(Weekday(0), 0) == 6  # n<1 clamps to first
                and may.nth_weekday(4, 5) == 31  # ints work; 5th Friday = 31st
            )
        return super().condition(feature, *args, **kwargs)


class FindsNthWeekdayMixin(FindsNthWeekdayMixinBase, ABC):
    negative_finds_nth_weekday: bool = False

    @pytest.mark.feature_calendar_math
    def test_finds_nth_weekday(self, working_weekday: None) -> None:
        """nth_weekday locates the nth weekday from names, ints or instances."""
        assert self.validate("finds_nth_weekday", working_weekday=working_weekday)


class NoFindsNthWeekdayMixin(FindsNthWeekdayMixinBase, ABC):
    negative_finds_nth_weekday: bool = True

    @pytest.mark.feature_calendar_math
    def test_finds_nth_weekday(self, working_weekday: None) -> None:
        """Negated variant: nth_weekday must not find the right day."""
        assert self.validate("finds_nth_weekday", working_weekday=working_weekday)


class FailsNthWeekdayBeyondMonthMixinBase(Mixin, ABC):
    """Feature: asking for an occurrence past the end of the month raises."""

    fail_fails_nth_weekday_beyond_month: type[BaseException] = ValueError

    @pytest.fixture
    @abstractmethod
    def working_weekday(self) -> None: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_nth_weekday_beyond_month":
            FixedMonth(5, 2024).nth_weekday("monday", 6)  # only 4 Mondays fit
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsNthWeekdayBeyondMonthMixin(FailsNthWeekdayBeyondMonthMixinBase, ABC):
    negative_fails_nth_weekday_beyond_month: bool = False

    @pytest.mark.feature_calendar_math
    def test_fails_nth_weekday_beyond_month(self, working_weekday: None) -> None:
        """Positive variant (unused in practice)."""
        assert self.validate("fails_nth_weekday_beyond_month", working_weekday=working_weekday)


class NoFailsNthWeekdayBeyondMonthMixin(FailsNthWeekdayBeyondMonthMixinBase, ABC):
    negative_fails_nth_weekday_beyond_month: bool = True  # asserting variant

    @pytest.mark.feature_calendar_math
    def test_fails_nth_weekday_beyond_month(self, working_weekday: None) -> None:
        """A non-existent nth occurrence raises ValueError."""
        assert self.validate("fails_nth_weekday_beyond_month", working_weekday=working_weekday)


class FailsWeekdayMathWithoutYearMixinBase(Mixin, ABC):
    """Feature: both nth_weekday and last_nth_weekday refuse to run without a
    year (these guards fire before any other logic, so they work despite the
    defects in the rest of last_nth_weekday; see REPORT.md D5)."""

    fail_fails_weekday_math_without_year: type[BaseException] = ValueError

    @pytest.fixture
    @abstractmethod
    def weekday_math_call(self) -> str:
        """Which method to invoke: 'nth_weekday' or 'last_nth_weekday'."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_weekday_math_without_year":
            month = FixedMonth(5)  # no year attached
            getattr(month, kwargs["weekday_math_call"])(0)
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsWeekdayMathWithoutYearMixin(FailsWeekdayMathWithoutYearMixinBase, ABC):
    negative_fails_weekday_math_without_year: bool = False

    @pytest.mark.feature_calendar_math
    def test_fails_weekday_math_without_year(self, weekday_math_call: str) -> None:
        """Positive variant (unused in practice)."""
        assert self.validate("fails_weekday_math_without_year", weekday_math_call=weekday_math_call)


class NoFailsWeekdayMathWithoutYearMixin(FailsWeekdayMathWithoutYearMixinBase, ABC):
    negative_fails_weekday_math_without_year: bool = True  # asserting variant

    @pytest.mark.feature_calendar_math
    def test_fails_weekday_math_without_year(self, weekday_math_call: str) -> None:
        """Weekday math without a year raises ValueError up front."""
        assert self.validate("fails_weekday_math_without_year", weekday_math_call=weekday_math_call)


class MonthCalendarMixins(
    ComputesMonthrangeMixin,
    FindsNthWeekdayMixin,
    NoFailsNthWeekdayBeyondMonthMixin,
    ABC,
):
    """Group: Month's calendar computations."""


class TestMonth(
    PlainNumericComponentMixins,
    NamedComponentMixins,
    YearedComponentMixins,
    MonthCalendarMixins,
):
    """Month = numeric + naming + optional-year + calendar contracts."""

    # Named components accept strings, so the plain-numeric rejection flips.
    negative_rejects_string_values: bool = True

    @pytest.fixture
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]:
        return FixedMonth

    @pytest.fixture
    def yeared_cls(self) -> type[FixedMonth]:
        return FixedMonth

    @pytest.fixture
    def working_weekday(self, mocker: MockerFixture) -> None:
        """Temporarily restore the intended Weekday name table (undone by
        pytest-mock after each test), since Month.nth_weekday hardcodes the
        shipped-but-broken Weekday class (REPORT.md D1)."""
        mocker.patch.object(Weekday, "_NAMES", list(WEEKDAY_NAMES))
        mocker.patch.object(Weekday, "_LOOKUP", {n: i for i, n in enumerate(WEEKDAY_NAMES)})

    @pytest.fixture
    def min_value(self) -> int:
        return 1

    @pytest.fixture
    def max_value(self) -> int:
        return 12

    @pytest.fixture
    def in_range_value(self) -> int:
        return 5

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 9

    @pytest.fixture
    def safe_delta(self) -> int:
        # 5 +/- 3 stays inside 1..12.
        return 3

    @pytest.fixture
    def sample_name(self) -> str:
        return "may"

    @pytest.fixture
    def sample_name_int(self) -> int:
        return 5

    @pytest.fixture
    def other_name(self) -> str:
        return "september"

    @pytest.fixture
    def other_name_int(self) -> int:
        return 9


class TestMonthNthWeekday(NoFailsWeekdayMathWithoutYearMixin):
    """Method-focused: Month.nth_weekday's year guard."""

    @pytest.fixture
    def weekday_math_call(self) -> str:
        return "nth_weekday"


class TestMonthLastNthWeekday(NoFailsWeekdayMathWithoutYearMixin):
    """Method-focused: Month.last_nth_weekday's year guard."""

    @pytest.fixture
    def weekday_math_call(self) -> str:
        return "last_nth_weekday"
