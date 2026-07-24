"""
SUGGESTED features for the component classes (see REPORT.md, "Suggested
features"). None of these exist yet: every test is marked `suggested_feature`
and `xfail` so the suite acknowledges them as currently failing. Type errors
are ignored where the code references not-yet-existing attributes.

Suggestions run against the Fixed* helpers so that, once implemented, the
tests fail/pass on the feature itself rather than on defect D1.
"""
import pytest
from abc import ABC
from datetime import date
from typing import Any

from test_utils import Mixin
import dateutils
from helpers import FixedMonth, FixedWeekday, FixedSeason, FixedHour


xfail_missing = pytest.mark.xfail(reason="suggested feature not implemented yet")


# S1 --------------------------------------------------------------------------
class ExportsDurationMixinBase(Mixin, ABC):
    """Suggested: re-export the duration module from the package root
    (add `from .duration import *` to __init__.py)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "exports_duration":
            return hasattr(dateutils, "Duration")
        return super().condition(feature, *args, **kwargs)


class ExportsDurationMixin(ExportsDurationMixinBase, ABC):
    negative_exports_duration: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_exports
    def test_exports_duration(self) -> None:
        """Duration should be importable from the package root."""
        assert self.validate("exports_duration")


class NoExportsDurationMixin(ExportsDurationMixinBase, ABC):
    negative_exports_duration: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_exports
    def test_exports_duration(self) -> None:
        """Negated variant."""
        assert self.validate("exports_duration")


@xfail_missing
class TestPackageExportsDuration(ExportsDurationMixin):
    """S1: `dateutils.Duration` should exist."""


# S2 --------------------------------------------------------------------------
class BuildsFromDateMixinBase(Mixin, ABC):
    """Suggested: `from_date` classmethods for datetime interop, e.g.
    Weekday.from_date(d) and Month.from_date(d) (carrying the year)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "builds_from_date":
            d = date(2024, 5, 13)  # a Monday in May
            weekday = FixedWeekday.from_date(d)  # type: ignore[attr-defined]
            month = FixedMonth.from_date(d)  # type: ignore[attr-defined]
            return weekday.str_id == "monday" and month.str_id == "may" and month.year == 2024
        return super().condition(feature, *args, **kwargs)


class BuildsFromDateMixin(BuildsFromDateMixinBase, ABC):
    negative_builds_from_date: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_datetime_parity
    def test_builds_from_date(self) -> None:
        """Components should build directly from datetime.date objects."""
        assert self.validate("builds_from_date")


class NoBuildsFromDateMixin(BuildsFromDateMixinBase, ABC):
    negative_builds_from_date: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_datetime_parity
    def test_builds_from_date(self) -> None:
        """Negated variant."""
        assert self.validate("builds_from_date")


@xfail_missing
class TestComponentsFromDate(BuildsFromDateMixin):
    """S2: Weekday.from_date / Month.from_date should exist."""


# S3 --------------------------------------------------------------------------
class DerivesSeasonForMonthMixinBase(Mixin, ABC):
    """Suggested: Season.for_month(month) mapping meteorological seasons
    (Mar-May spring, Jun-Aug summer, Sep-Nov autumn, Dec-Feb winter)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "derives_season_for_month":
            return (
                FixedSeason.for_month(FixedMonth(4)).str_id == "spring"  # type: ignore[attr-defined]
                and FixedSeason.for_month(FixedMonth(12)).str_id == "winter"  # type: ignore[attr-defined]
            )
        return super().condition(feature, *args, **kwargs)


class DerivesSeasonForMonthMixin(DerivesSeasonForMonthMixinBase, ABC):
    negative_derives_season_for_month: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_calendar_math
    def test_derives_season_for_month(self) -> None:
        """Seasons should be derivable from months."""
        assert self.validate("derives_season_for_month")


class NoDerivesSeasonForMonthMixin(DerivesSeasonForMonthMixinBase, ABC):
    negative_derives_season_for_month: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_calendar_math
    def test_derives_season_for_month(self) -> None:
        """Negated variant."""
        assert self.validate("derives_season_for_month")


@xfail_missing
class TestSeasonForMonth(DerivesSeasonForMonthMixin):
    """S3: Season.for_month should exist."""


# S4 --------------------------------------------------------------------------
class ReportsMeridiemMixinBase(Mixin, ABC):
    """Suggested: Hour.is_am()/is_pm() predicates to complement to_12h()."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "reports_meridiem":
            return (
                FixedHour(3).is_am()  # type: ignore[attr-defined]
                and FixedHour(15).is_pm()  # type: ignore[attr-defined]
                and not FixedHour(15).is_am()  # type: ignore[attr-defined]
            )
        return super().condition(feature, *args, **kwargs)


class ReportsMeridiemMixin(ReportsMeridiemMixinBase, ABC):
    negative_reports_meridiem: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_clock_format
    def test_reports_meridiem(self) -> None:
        """Hours should report AM/PM directly."""
        assert self.validate("reports_meridiem")


class NoReportsMeridiemMixin(ReportsMeridiemMixinBase, ABC):
    negative_reports_meridiem: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_clock_format
    def test_reports_meridiem(self) -> None:
        """Negated variant."""
        assert self.validate("reports_meridiem")


@xfail_missing
class TestHourMeridiem(ReportsMeridiemMixin):
    """S4: Hour.is_am / Hour.is_pm should exist."""


# S5 --------------------------------------------------------------------------
class OrdersComponentsMixinBase(Mixin, ABC):
    """Suggested: rich ordering (<, <=, >, >=) on components so that e.g.
    weekdays sort naturally - currently only ==/!= are supported."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "orders_components":
            return (
                FixedWeekday("monday") < FixedWeekday("friday")  # type: ignore[operator]
                and FixedMonth("march") <= FixedMonth("march")  # type: ignore[operator]
                and sorted([FixedHour(9), FixedHour(3)])[0] == FixedHour(3)  # type: ignore[type-var]
            )
        return super().condition(feature, *args, **kwargs)


class OrdersComponentsMixin(OrdersComponentsMixinBase, ABC):
    negative_orders_components: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_equality
    def test_orders_components(self) -> None:
        """Components should be orderable/sortable by int_id."""
        assert self.validate("orders_components")


class NoOrdersComponentsMixin(OrdersComponentsMixinBase, ABC):
    negative_orders_components: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_equality
    def test_orders_components(self) -> None:
        """Negated variant."""
        assert self.validate("orders_components")


@xfail_missing
class TestComponentOrdering(OrdersComponentsMixin):
    """S5: NumericDateComponentBase should implement ordering."""
