"""
Verification of REJECTED behavior (see REPORT.md for the defect register).

These tests intentionally pin down the *defective* behavior so the defects
are demonstrably present; they are NOT tests of expected behavior and should
be deleted once the defects are fixed. They are exempt from the standard
mixin architecture (assumed temporary) and are all marked with
`reject_verification`.
"""
import math
import pytest
from datetime import timedelta
from pytest_mock import MockerFixture

from dateutils.base import NumericDateComponentBase
from dateutils.month import Month
from dateutils.weekday import Weekday
from dateutils.season import Season
from dateutils.hour import Hour
from dateutils.minute import Minute
from dateutils.duration import Duration
from helpers import FixedMonth, FixedSeason, FixedWeekday, WEEKDAY_NAMES, MONTH_NAMES


pytestmark = pytest.mark.reject_verification


# --- D1: get_args() on PEP 695 aliases -> empty _NAMES -> unusable classes ---
class TestD1NamedClassesUnconstructible:
    def test_name_tables_are_empty(self) -> None:
        """typing.get_args(<lazy type alias>) returns (), leaving every
        shipped named component without a single name."""
        assert Month._NAMES == []
        assert Weekday._NAMES == []
        assert Season._NAMES == []
        assert Hour._NAMES == []

    def test_int_construction_crashes(self) -> None:
        """With no names to map to, even valid ints explode with IndexError."""
        for cls, value in ((Month, 1), (Weekday, 0), (Season, 1), (Hour, 0)):
            with pytest.raises(IndexError):
                cls(value)

    def test_valid_names_are_rejected(self) -> None:
        """Every canonical name is 'invalid' because the lookup is empty."""
        with pytest.raises(ValueError):
            Weekday("monday")
        with pytest.raises(ValueError):
            Month("january")


# --- D2: size() off-by-one -> broken wrap-around arithmetic -------------------
class TestD2SizeOffByOne:
    def test_size_is_one_short(self) -> None:
        """size() returns _MAX - _MIN; a 0..59 component reports 59 values."""
        assert Minute.size() == 59  # should be 60

    def test_wrap_lands_on_wrong_value(self) -> None:
        """Crossing the range boundary skips a value (modulo base too small)."""
        assert (FixedWeekday(6) + 1).str_id == "tuesday"  # should be monday
        assert (FixedMonth(12) + 1).str_id == "february"  # should be january
        assert (FixedMonth(1) - 1).str_id == "november"  # should be december

    def test_in_range_result_on_max_is_corrupted(self) -> None:
        """Even a shift that legitimately lands ON the max wraps to min."""
        assert (Minute(50) + 9).int_id == 0  # should be 59, no wrap involved

    def test_season_wrap_also_skips(self) -> None:
        """Seasons wrap into the wrong quarter too (covers Season._apply_loop
        being invoked on a year-less result)."""
        assert (FixedSeason(4) + 1).str_id == "summer"  # should be spring


# --- D3: Month.monthrange() year guard is inverted ---------------------------
class TestD3InvertedFebruaryGuard:
    def test_february_with_year_raises(self) -> None:
        """Setting the year (the documented requirement!) triggers the error."""
        with pytest.raises(ValueError):
            FixedMonth(2, 2024).monthrange()
        with pytest.raises(ValueError):
            len(FixedMonth(2, 2024))

    def test_february_without_year_silently_uses_1970(self) -> None:
        """The case the docstring says must raise instead returns 1970's 28."""
        assert len(FixedMonth(2)) == 28


# --- D4: __add__ drops the year; _apply_loop year bump is dead code ----------
class TestD4YearLostOnShift:
    def test_shift_discards_year(self) -> None:
        """base.__add__ rebuilds via type(self)(wrapped_int): year is gone."""
        assert (FixedMonth(5, 2024) + 1).year is None

    def test_wrap_cannot_bump_year(self) -> None:
        """Even when _apply_loop fires, the result has no year to adjust."""
        assert (FixedMonth(12, 2024) + 1).year is None  # should be 2025
        assert (FixedSeason(4, 2024) + 1).year is None  # should be 2025

    def test_apply_loop_logic_exists_but_is_unreachable(self) -> None:
        """Called directly, _apply_loop does bump the year - proving the
        intent - but no public path ever reaches it with a year set."""
        month = FixedMonth(3, 2024)
        season = FixedSeason(2, 2024)
        assert month._apply_loop(2).year == 2026
        assert season._apply_loop(-1).year == 2023

    def test_create_from_also_drops_year(self) -> None:
        """The generic copy path loses the year as well, so the 'copy' does
        not even compare equal to its source."""
        original = FixedMonth(5, 2024)
        copy = FixedMonth.create_from(original)
        assert copy.year is None
        assert copy != original


# --- D5: Month.last_nth_weekday can never succeed ----------------------------
class _YearPropagatingMonth(FixedMonth):
    """What Month would behave like if __add__ kept the year (D4 fixed) and
    size() were irrelevant (no wrap in these scenarios). Used only to prove
    the remainder of last_nth_weekday would work."""

    def __add__(self, delta: int) -> "_YearPropagatingMonth":
        result = super().__add__(delta)
        result.year = self.year  # re-attach what base.__add__ dropped
        return result


class TestD5LastNthWeekdayAlwaysRaises:
    @pytest.fixture
    def working_weekday(self, mocker: MockerFixture) -> None:
        """Restore Weekday's name table (D1) so the method can even start."""
        mocker.patch.object(Weekday, "_NAMES", list(WEEKDAY_NAMES))
        mocker.patch.object(Weekday, "_LOOKUP", {n: i for i, n in enumerate(WEEKDAY_NAMES)})

    def test_always_raises_despite_valid_input(self, working_weekday: None) -> None:
        """The internally-built next month has no year (D4), so the nested
        nth_weekday call always raises - for any valid input."""
        with pytest.raises(ValueError, match="Year must be set"):
            FixedMonth(5, 2024).last_nth_weekday("friday")

    def test_would_work_if_year_propagated(self, working_weekday: None) -> None:
        """With the year re-attached, the remaining logic is sound: the last
        Friday of May 2024 is the 31st, and impossible occurrences raise the
        intended not-exists error."""
        assert _YearPropagatingMonth(5, 2024).last_nth_weekday("friday") == 31
        assert _YearPropagatingMonth(5, 2024).last_nth_weekday("friday", 0) == 31  # n<1 clamps
        assert _YearPropagatingMonth(5, 2024).last_nth_weekday("friday", 5) == 3
        with pytest.raises(ValueError, match="does not exist"):
            _YearPropagatingMonth(5, 2024).last_nth_weekday("friday", 6)


# --- D6: total_seconds() uses 8640 seconds per day ---------------------------
class TestD6DaysConstantTypo:
    def test_one_day_is_ten_times_too_short(self) -> None:
        assert Duration(days=1).total_seconds() == 8640  # should be 86400

    def test_inconsistent_with_weeks(self) -> None:
        """Seven days and one week are the same duration yet disagree."""
        assert Duration(days=7).total_seconds() == 604800  # simplifies to 1 week
        assert Duration(days=3).total_seconds() * 7 != Duration(weeks=3).total_seconds()

    def test_comparisons_inherit_the_error(self) -> None:
        """Ordering against timedelta is wrong for day-bearing durations."""
        assert Duration(days=1) < timedelta(hours=3)  # 1 day compares as 2.4h


# --- D7: simplify() corrupts negative fractional seconds ---------------------
class TestD7NegativeFractionCorruption:
    def test_negative_half_second_becomes_positive(self) -> None:
        """int() truncates toward zero, so the borrowed minute is skipped and
        -0.5s re-emerges as +59.5s with no compensating -1 minute."""
        simplified = Duration(seconds=-0.5).simplify()
        assert simplified.seconds == 59.5
        assert simplified.minutes == 0  # should be -1 if 59.5 were kept

    def test_negative_integers_are_fine_by_contrast(self) -> None:
        """For integer seconds the // borrow works: the result is a
        mixed-sign form (-1 week + 6d 23h 59m 30s) that still nets to -30s
        under correct unit sizes - demonstrating the corruption is specific
        to fractions."""
        s = Duration(seconds=-30).simplify()
        netted = s.seconds + s.minutes * 60 + s.hours * 3600 + s.days * 86400 + s.weeks * 604800
        assert netted == -30
        # The fractional case nets to +59.5 under the same arithmetic: wrong.
        f = Duration(seconds=-0.5).simplify()
        netted_f = f.seconds + f.minutes * 60 + f.hours * 3600 + f.days * 86400 + f.weeks * 604800
        assert netted_f == 59.5


# --- D8: __neg__ round-trips through total_seconds ---------------------------
class TestD8NegationRequiresExactness:
    def test_cannot_negate_month_durations(self) -> None:
        """Negating months=1 to months=-1 needs no fixed length, yet raises."""
        with pytest.raises(ValueError):
            -Duration(months=1)

    def test_subtraction_of_inexact_durations_raises(self) -> None:
        """__sub__ negates its operand, so month-for-month subtraction dies."""
        with pytest.raises(ValueError):
            Duration(months=3) - Duration(months=1)

    def test_abs_of_negative_compounds_with_d6(self) -> None:
        """abs() flows through __neg__/total_seconds; with D6 in the mix a
        -5s duration 'absolutes' to 77765 seconds."""
        assert abs(Duration(seconds=-5)).total_seconds() == 77765  # should be 5
