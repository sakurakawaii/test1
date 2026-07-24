"""
Tests for SUGGESTED features that do not exist yet (see REPORT.md §Suggested
Features). Every test is marked `suggested_feature` and `xfail`, acknowledging
that it currently fails; once a feature is implemented its test flips to
XPASS (strict=True turns that into a hard reminder to promote the test).

Type errors are ignored throughout since the attributes do not exist yet.
"""
# mypy: ignore-errors
from abc import ABC
from datetime import date, timedelta
from typing import Any

import pytest

from datecomponents.duration import Duration
from tests.test_hour import UsableHour
from tests.test_month import UsableMonth
from tests.test_season import UsableSeason
from tests.test_weekday import UsableWeekday
from tests.test_utils import Mixin

suggested = pytest.mark.suggested_feature
currently_failing = pytest.mark.xfail(
    raises=(AttributeError, TypeError, NotImplementedError),
    reason="suggested feature - not implemented yet",
    strict=True,
)


# --- suggestion S1: Weekday.is_weekend() ----------------------------------------

class IsWeekendMixinBase(Mixin, ABC):
    """Weekday.is_weekend() -> True for saturday/sunday."""

    @pytest.fixture
    def weekday_subject(self) -> UsableWeekday:
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "is_weekend":
            return kwargs["weekday_subject"].is_weekend()
        return super().condition(feature, *args, **kwargs)


class IsWeekendMixin(IsWeekendMixinBase, ABC):
    negative_is_weekend: bool = False

    @suggested
    @currently_failing
    @pytest.mark.calendar
    def test_is_weekend(self, weekday_subject: UsableWeekday) -> None:
        """Saturday/Sunday report as weekend (negated for midweek days)."""
        assert self.validate("is_weekend", weekday_subject=weekday_subject)


class NoIsWeekendMixin(IsWeekendMixin, ABC):
    negative_is_weekend: bool = True


class TestWeekdayIsWeekend(IsWeekendMixin):
    @pytest.fixture
    def weekday_subject(self) -> UsableWeekday:
        return UsableWeekday("saturday")


class TestWeekdayIsWeekendMidweek(TestWeekdayIsWeekend):
    """Inherits the test; a midweek day must answer False."""

    negative_is_weekend: bool = True

    @pytest.fixture
    def weekday_subject(self) -> UsableWeekday:
        return UsableWeekday("wednesday")


# --- suggestion S2: Weekday.from_date() classmethod ------------------------------

class WeekdayFromDateMixinBase(Mixin, ABC):
    """Weekday.from_date(date) -> the matching Weekday (datetime parity)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "weekday_from_date":
            # 2024-03-11 was a Monday.
            return UsableWeekday.from_date(date(2024, 3, 11)).str_id == "monday"
        return super().condition(feature, *args, **kwargs)


class WeekdayFromDateMixin(WeekdayFromDateMixinBase, ABC):
    negative_weekday_from_date: bool = False

    @suggested
    @currently_failing
    @pytest.mark.construction
    @pytest.mark.static
    def test_weekday_from_date(self) -> None:
        """A date maps onto its weekday via a classmethod constructor."""
        assert self.validate("weekday_from_date")


class NoWeekdayFromDateMixin(WeekdayFromDateMixin, ABC):
    negative_weekday_from_date: bool = True


class TestWeekdayFromDate(WeekdayFromDateMixin):
    pass


# --- suggestion S3: Month.season() <-> Season.months() ----------------------------

class MonthSeasonBridgeMixinBase(Mixin, ABC):
    """Month.season() and Season.months() convert between the two components."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "month_season_bridge":
            # Meteorological seasons: december belongs to winter, and summer
            # spans june-august.
            winter = UsableMonth("december").season()
            summer_months = UsableSeason("summer").months()
            return (
                winter.str_id == "winter"
                and [m.str_id for m in summer_months] == ["june", "july", "august"]
            )
        return super().condition(feature, *args, **kwargs)


class MonthSeasonBridgeMixin(MonthSeasonBridgeMixinBase, ABC):
    negative_month_season_bridge: bool = False

    @suggested
    @currently_failing
    @pytest.mark.calendar
    def test_month_season_bridge(self) -> None:
        """Months know their meteorological season and seasons their months."""
        assert self.validate("month_season_bridge")


class NoMonthSeasonBridgeMixin(MonthSeasonBridgeMixin, ABC):
    negative_month_season_bridge: bool = True


class TestMonthSeasonBridge(MonthSeasonBridgeMixin):
    pass


# --- suggestion S4: Hour.is_am() / Hour.is_pm() -------------------------------------

class HourMeridiemMixinBase(Mixin, ABC):
    """Hour.is_am()/is_pm() complement the existing 12h/24h conversions."""

    @pytest.fixture
    def hour_subject(self) -> UsableHour:
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "hour_meridiem":
            subject: UsableHour = kwargs["hour_subject"]
            # The two predicates must be mutually exclusive.
            return subject.is_am() and not subject.is_pm()
        return super().condition(feature, *args, **kwargs)


class HourMeridiemMixin(HourMeridiemMixinBase, ABC):
    negative_hour_meridiem: bool = False

    @suggested
    @currently_failing
    @pytest.mark.conversion
    def test_hour_meridiem(self, hour_subject: UsableHour) -> None:
        """Morning hours are am and not pm (negated for afternoon hours)."""
        assert self.validate("hour_meridiem", hour_subject=hour_subject)


class NoHourMeridiemMixin(HourMeridiemMixin, ABC):
    negative_hour_meridiem: bool = True


class TestHourMeridiemMorning(HourMeridiemMixin):
    @pytest.fixture
    def hour_subject(self) -> UsableHour:
        return UsableHour("9am")


class TestHourMeridiemAfternoon(TestHourMeridiemMorning):
    """Inherits the test; afternoon hours must answer the other way around."""

    negative_hour_meridiem: bool = True

    @pytest.fixture
    def hour_subject(self) -> UsableHour:
        return UsableHour("9pm")


# --- suggestion S5: Duration.total_days() --------------------------------------------

class DurationTotalDaysMixinBase(Mixin, ABC):
    """Duration.total_days() mirrors total_seconds at day granularity."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "duration_total_days":
            return Duration(weeks=2).total_days() == 14.0
        return super().condition(feature, *args, **kwargs)


class DurationTotalDaysMixin(DurationTotalDaysMixinBase, ABC):
    negative_duration_total_days: bool = False

    @suggested
    @currently_failing
    @pytest.mark.conversion
    def test_duration_total_days(self) -> None:
        """Two weeks total exactly 14 days."""
        assert self.validate("duration_total_days")


class NoDurationTotalDaysMixin(DurationTotalDaysMixin, ABC):
    negative_duration_total_days: bool = True


class TestDurationTotalDays(DurationTotalDaysMixin):
    pass


# --- suggestion S6: Duration floor-division ---------------------------------------------

class DurationFloordivMixinBase(Mixin, ABC):
    """duration // duration -> how many whole spans fit (like ints)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "duration_floordiv":
            return (
                Duration(minutes=5) // Duration(minutes=2) == 2
                and Duration(minutes=5) // timedelta(minutes=2) == 2
            )
        return super().condition(feature, *args, **kwargs)


class DurationFloordivMixin(DurationFloordivMixinBase, ABC):
    negative_duration_floordiv: bool = False

    @suggested
    @currently_failing
    @pytest.mark.arithmetic
    def test_duration_floordiv(self) -> None:
        """// counts whole fits of one span inside another."""
        assert self.validate("duration_floordiv")


class NoDurationFloordivMixin(DurationFloordivMixin, ABC):
    negative_duration_floordiv: bool = True


class TestDurationFloordiv(DurationFloordivMixin):
    pass
