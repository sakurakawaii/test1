"""
Temporary verification tests for the defects reported in REPORT.md.

Each test PROVES that a reported defect is present in the shipped code; none
of this is expected behavior. The tests are deliberately plain (no mixin
architecture) because they should be deleted as the defects are fixed. They
are all marked `reject_verification` so they can be deselected once repairs
land: `pytest -m "not reject_verification"`.
"""
import pytest

from datecomponents.base import NumericDateComponentBase
from datecomponents.duration import Duration
from datecomponents.hour import Hour
from datecomponents.minute import Minute
from datecomponents.month import Month
from datecomponents.season import Season
from datecomponents.weekday import Weekday
from tests.test_month import UsableMonth
from tests.test_season import UsableSeason
from tests.test_weekday import UsableWeekday


@pytest.mark.reject_verification
class TestD1NamedClassesAreUnusable:
    """
    D1: `get_args()` on a PEP 695 `type` alias returns (), leaving _NAMES
    empty, so no shipped named component can be constructed on Python 3.12+.
    (weekday.py:15, month.py:17, season.py:10, hour.py:18)
    """

    def test_names_lists_are_empty(self) -> None:
        assert Month._NAMES == []
        assert Weekday._NAMES == []
        assert Season._NAMES == []
        assert Hour._NAMES == []

    def test_int_construction_crashes(self) -> None:
        # Int input clamps fine but the empty _NAMES lookup then explodes.
        for cls, value in ((Month, 5), (Weekday, 3), (Season, 2), (Hour, 13)):
            with pytest.raises(IndexError):
                cls(value)

    def test_name_construction_rejects_every_valid_name(self) -> None:
        # The names promised by the type aliases are all "invalid".
        with pytest.raises(ValueError):
            Month("may")
        with pytest.raises(ValueError):
            Weekday("monday")
        with pytest.raises(ValueError):
            Season("summer")
        with pytest.raises(ValueError):
            Hour("noon")


@pytest.mark.reject_verification
class TestD2SizeOffByOneBreaksWrapAround:
    """
    D2a: size() omits the +1 for inclusive bounds (base.py:46), so every
    wrap-around in __add__/__sub__ (base.py:83-85) lands on the wrong value.
    """

    def test_size_is_one_short(self) -> None:
        # Minute spans 0..59 = 60 values, but size() says 59.
        assert Minute.size() == 59

    def test_add_wrapping_lands_wrong(self) -> None:
        # 59 + 1 should wrap to 0; the off-by-one lands on 1.
        assert int(Minute(59) + 1) == 1

    def test_add_landing_on_max_wraps_spuriously(self) -> None:
        # 50 + 9 = 59 is still in range and should NOT wrap at all.
        assert int(Minute(50) + 9) == 0

    def test_sub_wrapping_lands_wrong(self) -> None:
        # 0 - 1 should wrap to 59; it lands on 58.
        assert int(Minute(0) - 1) == 58


@pytest.mark.reject_verification
class TestD2YearLostOnArithmetic:
    """
    D2b: __add__ rebuilds via `type(self)(wrapped_int)` (base.py:87), which
    never forwards the year, so Month/Season arithmetic silently drops it and
    the year-carrying `_apply_loop` overrides (month.py:102-103,
    season.py:32-33) can never actually adjust anything.
    """

    def test_month_add_drops_year(self) -> None:
        result = UsableMonth("march", 2024) + 1
        assert result.int_id == 4  # the month itself is right (no wrap)...
        assert result.year is None  # ...but the year is gone.

    def test_month_wrap_does_not_carry_year(self) -> None:
        # december 2024 + 1 should be january 2025; with D2a+D2b it is
        # february (wrong value) of no year at all.
        result = UsableMonth("december", 2024) + 1
        assert result.str_id == "february"
        assert result.year is None

    def test_season_wrap_does_not_carry_year(self) -> None:
        # winter 2024 + 1 should be spring 2025; with D2a+D2b it is
        # summer (wrong value) of no year at all.
        result = UsableSeason("winter", 2024) + 1
        assert result.str_id == "summer"
        assert result.year is None

    def test_weekday_wrap_lands_wrong(self) -> None:
        # sunday + 1 should be monday; D2a lands on tuesday instead.
        assert (UsableWeekday("sunday") + 1).str_id == "tuesday"


@pytest.mark.reject_verification
class TestD3MonthrangeFebruaryConditionInverted:
    """
    D3: monthrange() raises for February WITH a year and silently uses 1970
    for February WITHOUT one - the exact opposite of its docstring
    (month.py:42-43: `and self.has_year()` should be `and not ...`).
    """

    def test_february_with_year_raises(self) -> None:
        with pytest.raises(ValueError, match="Year must be set"):
            UsableMonth("february", 2024).monthrange()

    def test_february_without_year_silently_uses_1970(self) -> None:
        # 1970 was not a leap year, so every year-less February is 28 days.
        assert UsableMonth("february").monthrange()[1] == 28

    def test_len_of_february_with_year_raises(self) -> None:
        # Collateral: the length of a fully specified February is unavailable.
        with pytest.raises(ValueError):
            len(UsableMonth("february", 2024))


@pytest.mark.reject_verification
class TestD4WeekdayHelpersUnreachable:
    """
    D4 (consequence of D1 + D2b): nth_weekday constructs the broken shipped
    Weekday internally (month.py:57), and last_nth_weekday additionally
    relies on `self + 1` keeping the year (month.py:88-89). Both fail for
    every input that passes the year guard, leaving month.py:59-70 and
    month.py:84-96 unreachable.
    """

    def test_nth_weekday_rejects_valid_weekday_names(self) -> None:
        # "monday" is a valid weekday name, yet D1 makes Weekday reject it.
        with pytest.raises(ValueError, match="Invalid weekday name"):
            UsableMonth("march", 2024).nth_weekday("monday", 2)

    def test_nth_weekday_crashes_on_weekday_ints(self) -> None:
        with pytest.raises(IndexError):
            UsableMonth("march", 2024).nth_weekday(0)

    def test_last_nth_weekday_always_raises_for_yeared_months(self) -> None:
        # Even if Weekday worked, `self + 1` drops the year (D2b), so the
        # inner nth_weekday call would hit its own year guard.
        with pytest.raises((ValueError, IndexError)):
            UsableMonth("march", 2024).last_nth_weekday("friday")


@pytest.mark.reject_verification
class TestD5DaysConvertAt8640Seconds:
    """
    D5: total_seconds() multiplies days by 8640 instead of 86400
    (duration.py:52), shrinking any simplified day remainder by 10x.
    """

    def test_one_day_totals_8640_seconds(self) -> None:
        assert Duration(days=1).total_seconds() == 8640

    def test_day_remainders_corrupt_larger_spans(self) -> None:
        # 25 hours simplifies to 1 day + 1 hour; the day shrinks to 8640s.
        assert Duration(hours=25).total_seconds() == 8640 + 3600
        # Only whole weeks survive: 7 days fold into a week and are correct.
        assert Duration(days=7).total_seconds() == 604_800


@pytest.mark.reject_verification
class TestM1DurationNotExported:
    """M1 (minor): the package __init__ never imports duration."""

    def test_duration_missing_from_package_namespace(self) -> None:
        import datecomponents

        assert not hasattr(datecomponents, "Duration")


@pytest.mark.reject_verification
class TestM2CreateFromBoolInconsistency:
    """
    M2 (minor): the constructor rejects bools by design, but create_from
    falls through to `cls(int(value))` (base.py:41-43) and quietly accepts
    them, bypassing that guard.
    """

    def test_create_from_accepts_bool_despite_constructor_guard(self) -> None:
        with pytest.raises(TypeError):
            Minute(True)  # type: ignore[arg-type]  # the guard works here...
        assert Minute.create_from(True).int_id == 1  # type: ignore[arg-type]

    def test_base_class_guard_is_reachable_directly(self) -> None:
        # The same guard on the plain base class, for completeness.
        with pytest.raises(TypeError):
            NumericDateComponentBase(None)  # type: ignore[arg-type]
