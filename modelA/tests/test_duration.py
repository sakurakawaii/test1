"""Tests for dateutils/duration.py.

Durations whose *simplified* form has a non-zero `days` field are excluded
from total_seconds-dependent assertions: the days->seconds factor is defective
(REPORT.md D6), as is negative-total handling that flows through it (D7/D8).
All values here are chosen to be day-free after simplification (sub-day
amounts or exact week multiples), where behavior is correct.
"""
import pytest
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from test_utils import Mixin
from dateutils.duration import Duration


# ---------------------------------------------------------------- construction
class BuildsFromOtherFormsMixinBase(Mixin, ABC):
    """Feature: from_seconds/from_timedelta/create_from build Durations
    (static test: all constructors are class-level)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "builds_from_other_forms":
            existing = Duration(minutes=2)
            from_td = Duration.from_timedelta(timedelta(minutes=1, seconds=1, microseconds=500_000))
            return (
                Duration.from_seconds(75).total_seconds() == 75
                and from_td.total_seconds() == 61.5
                and Duration.create_from(30) == Duration(seconds=30)
                and Duration.create_from(timedelta(seconds=45)) == Duration(seconds=45)
                and Duration.create_from(existing) is existing  # passthrough
            )
        return super().condition(feature, *args, **kwargs)


class BuildsFromOtherFormsMixin(BuildsFromOtherFormsMixinBase, ABC):
    negative_builds_from_other_forms: bool = False

    @pytest.mark.feature_duration_construction
    @pytest.mark.static
    def test_builds_from_other_forms(self) -> None:
        """Durations build from numbers, timedeltas and other Durations."""
        assert self.validate("builds_from_other_forms")


class NoBuildsFromOtherFormsMixin(BuildsFromOtherFormsMixinBase, ABC):
    negative_builds_from_other_forms: bool = True

    @pytest.mark.feature_duration_construction
    @pytest.mark.static
    def test_builds_from_other_forms(self) -> None:
        """Negated variant: construction helpers must not work."""
        assert self.validate("builds_from_other_forms")


class FailsCreateFromUnsupportedMixinBase(Mixin, ABC):
    """Feature: create_from rejects unsupported types."""

    fail_fails_create_from_unsupported: type[BaseException] = TypeError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_create_from_unsupported":
            Duration.create_from("ninety")  # type: ignore[arg-type]
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsCreateFromUnsupportedMixin(FailsCreateFromUnsupportedMixinBase, ABC):
    negative_fails_create_from_unsupported: bool = False

    @pytest.mark.feature_duration_construction
    @pytest.mark.static
    def test_fails_create_from_unsupported(self) -> None:
        """Positive variant (unused in practice)."""
        assert self.validate("fails_create_from_unsupported")


class NoFailsCreateFromUnsupportedMixin(FailsCreateFromUnsupportedMixinBase, ABC):
    negative_fails_create_from_unsupported: bool = True  # asserting variant

    @pytest.mark.feature_duration_construction
    @pytest.mark.static
    def test_fails_create_from_unsupported(self) -> None:
        """create_from raises TypeError for unsupported inputs."""
        assert self.validate("fails_create_from_unsupported")


# -------------------------------------------------------------------- simplify
class SimplifiesUnitsMixinBase(Mixin, ABC):
    """Feature: simplify() cascades fractions downward, carries overflow
    upward, and folds exact year/month lengths into days."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "simplifies_units":
            cascaded = Duration(days=1.5).simplify()  # 1.5d -> 1d 12h
            carried = Duration(seconds=3723).simplify()  # -> 1h 2m 3s
            weeks = Duration(days=9).simplify()  # -> 1w 2d
            folded = Duration(years=1, months=2, year_days=364, month_days=28).simplify()
            return (
                (cascaded.days, cascaded.hours) == (1, 12)
                and (carried.hours, carried.minutes, carried.seconds) == (1, 2, 3)
                and (weeks.weeks, weeks.days) == (1, 2)
                # 364 + 56 days = exactly 60 weeks; inexact units zero out
                and (folded.weeks, folded.years, folded.months) == (60, 0, 0)
            )
        return super().condition(feature, *args, **kwargs)


class SimplifiesUnitsMixin(SimplifiesUnitsMixinBase, ABC):
    negative_simplifies_units: bool = False

    @pytest.mark.feature_duration_simplify
    def test_simplifies_units(self) -> None:
        """Fractions cascade down, overflow carries up, exact lengths fold."""
        assert self.validate("simplifies_units")


class NoSimplifiesUnitsMixin(SimplifiesUnitsMixinBase, ABC):
    negative_simplifies_units: bool = True

    @pytest.mark.feature_duration_simplify
    def test_simplifies_units(self) -> None:
        """Negated variant: simplification must not normalize units."""
        assert self.validate("simplifies_units")


class ReportsSimplifiedStateMixinBase(Mixin, ABC):
    """Feature: is_simplified() distinguishes normalized instances, and
    repeated simplify() calls are stable (exercising the internal cache)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "reports_simplified_state":
            messy = Duration(seconds=90)
            tidy = Duration(minutes=1, seconds=30)
            return (
                not messy.is_simplified()
                and tidy.is_simplified()
                # calling twice must keep answering consistently
                and messy.simplify() == messy.simplify()
            )
        return super().condition(feature, *args, **kwargs)


class ReportsSimplifiedStateMixin(ReportsSimplifiedStateMixinBase, ABC):
    negative_reports_simplified_state: bool = False

    @pytest.mark.feature_duration_simplify
    def test_reports_simplified_state(self) -> None:
        """is_simplified reflects normalization; simplify is idempotent."""
        assert self.validate("reports_simplified_state")


class NoReportsSimplifiedStateMixin(ReportsSimplifiedStateMixinBase, ABC):
    negative_reports_simplified_state: bool = True

    @pytest.mark.feature_duration_simplify
    def test_reports_simplified_state(self) -> None:
        """Negated variant: simplified-state reporting must be wrong."""
        assert self.validate("reports_simplified_state")


# ----------------------------------------------------------------------- total
class ComputesTotalSecondsMixinBase(Mixin, ABC):
    """Feature: total_seconds()/to_timedelta() for day-free durations."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "computes_total_seconds":
            return (
                Duration(hours=1, minutes=2, seconds=3).total_seconds() == 3723
                and Duration(weeks=2).total_seconds() == 2 * 604800
                and Duration(minutes=90).to_timedelta() == timedelta(minutes=90)
            )
        return super().condition(feature, *args, **kwargs)


class ComputesTotalSecondsMixin(ComputesTotalSecondsMixinBase, ABC):
    negative_computes_total_seconds: bool = False

    @pytest.mark.feature_duration_total
    def test_computes_total_seconds(self) -> None:
        """Day-free totals convert exactly to seconds and timedeltas."""
        assert self.validate("computes_total_seconds")


class NoComputesTotalSecondsMixin(ComputesTotalSecondsMixinBase, ABC):
    negative_computes_total_seconds: bool = True

    @pytest.mark.feature_duration_total
    def test_computes_total_seconds(self) -> None:
        """Negated variant: totals must not be exact."""
        assert self.validate("computes_total_seconds")


class FailsTotalSecondsOnInexactUnitsMixinBase(Mixin, ABC):
    """Feature: totals refuse units that have no fixed length."""

    fail_fails_total_seconds_on_inexact_units: type[BaseException] = ValueError

    @pytest.fixture
    @abstractmethod
    def inexact_duration(self) -> Duration:
        """A Duration holding a unit with no fixed length."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_total_seconds_on_inexact_units":
            kwargs["inexact_duration"].total_seconds()
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsTotalSecondsOnInexactUnitsMixin(FailsTotalSecondsOnInexactUnitsMixinBase, ABC):
    negative_fails_total_seconds_on_inexact_units: bool = False

    @pytest.mark.feature_duration_total
    def test_fails_total_seconds_on_inexact_units(self, inexact_duration: Duration) -> None:
        """Positive variant (unused in practice)."""
        assert self.validate("fails_total_seconds_on_inexact_units", inexact_duration=inexact_duration)


class NoFailsTotalSecondsOnInexactUnitsMixin(FailsTotalSecondsOnInexactUnitsMixinBase, ABC):
    negative_fails_total_seconds_on_inexact_units: bool = True  # asserting variant

    @pytest.fixture
    def inexact_duration(self) -> Duration:
        """The inexact duration; overridden per test class."""
        raise NotImplementedError

    @pytest.mark.feature_duration_total
    def test_fails_total_seconds_on_inexact_units(self, inexact_duration: Duration) -> None:
        """total_seconds raises ValueError for units without fixed length."""
        assert self.validate("fails_total_seconds_on_inexact_units", inexact_duration=inexact_duration)


# ------------------------------------------------------------------- operators
class AddsAndSubtractsMixinBase(Mixin, ABC):
    """Feature: + and - combine Durations with Durations, numbers and
    timedeltas, from either side."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "adds_and_subtracts":
            return (
                Duration(minutes=1) + Duration(seconds=30) == Duration(seconds=90)
                and Duration(minutes=1) + 30 == Duration(seconds=90)
                and 30 + Duration(minutes=1) == Duration(seconds=90)  # __radd__
                and timedelta(seconds=30) + Duration(minutes=1) == Duration(seconds=90)
                and Duration(seconds=90) - 30 == Duration(minutes=1)
                and timedelta(seconds=90) - Duration(seconds=30) == Duration(minutes=1)  # __rsub__
                # exact year/month lengths survive addition
                and (Duration(years=1, year_days=364) + Duration(months=1, month_days=28)).total_seconds() == 56 * 604800
            )
        return super().condition(feature, *args, **kwargs)


class AddsAndSubtractsMixin(AddsAndSubtractsMixinBase, ABC):
    negative_adds_and_subtracts: bool = False

    @pytest.mark.feature_duration_operators
    def test_adds_and_subtracts(self) -> None:
        """+/- work with Durations, numbers and timedeltas on both sides."""
        assert self.validate("adds_and_subtracts")


class NoAddsAndSubtractsMixin(AddsAndSubtractsMixinBase, ABC):
    negative_adds_and_subtracts: bool = True

    @pytest.mark.feature_duration_operators
    def test_adds_and_subtracts(self) -> None:
        """Negated variant: arithmetic must not combine correctly."""
        assert self.validate("adds_and_subtracts")


class ScalesAndDividesMixinBase(Mixin, ABC):
    """Feature: scalar multiplication/division and duration-ratio division."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "scales_and_divides":
            return (
                Duration(minutes=2) * 2 == Duration(minutes=4)
                and 3 * Duration(seconds=10) == Duration(seconds=30)  # __rmul__
                and Duration(minutes=2) / 2 == Duration(minutes=1)
                and Duration(minutes=2) / Duration(seconds=60) == 2.0  # ratio
                and Duration(minutes=3) / timedelta(minutes=1) == 3.0
            )
        return super().condition(feature, *args, **kwargs)


class ScalesAndDividesMixin(ScalesAndDividesMixinBase, ABC):
    negative_scales_and_divides: bool = False

    @pytest.mark.feature_duration_operators
    def test_scales_and_divides(self) -> None:
        """* and / scale by numbers; / by durations yields a float ratio."""
        assert self.validate("scales_and_divides")


class NoScalesAndDividesMixin(ScalesAndDividesMixinBase, ABC):
    negative_scales_and_divides: bool = True

    @pytest.mark.feature_duration_operators
    def test_scales_and_divides(self) -> None:
        """Negated variant: scaling must not work."""
        assert self.validate("scales_and_divides")


class HandlesSignsMixinBase(Mixin, ABC):
    """Feature: unary sign operators for exact, sub-minute durations.
    (Negative totals that normalize through days are defective - D6/D7 -
    so only the well-behaved sub-minute window is asserted here.)"""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "handles_signs":
            return (
                -Duration(seconds=30) == Duration(seconds=-30)
                and +Duration(seconds=30) == Duration(seconds=30)
                and abs(Duration(minutes=5)) == Duration(minutes=5)  # already positive
            )
        return super().condition(feature, *args, **kwargs)


class HandlesSignsMixin(HandlesSignsMixinBase, ABC):
    negative_handles_signs: bool = False

    @pytest.mark.feature_duration_operators
    def test_handles_signs(self) -> None:
        """Unary -, + and abs() behave arithmetically for exact durations."""
        assert self.validate("handles_signs")


class NoHandlesSignsMixin(HandlesSignsMixinBase, ABC):
    negative_handles_signs: bool = True

    @pytest.mark.feature_duration_operators
    def test_handles_signs(self) -> None:
        """Negated variant: sign handling must be wrong."""
        assert self.validate("handles_signs")


class RejectsForeignOperandsMixinBase(Mixin, ABC):
    """Feature: every binary operator returns NotImplemented for unsupported
    operand types, surfacing as TypeError at the call site."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "rejects_foreign_operands":
            d = Duration(seconds=1)
            # One lambda per overload so every NotImplemented branch is hit.
            attempts: list[Any] = [
                lambda: d + "x", lambda: "x" + d,  # type: ignore[operator]
                lambda: d - "x", lambda: "x" - d,  # type: ignore[operator]
                lambda: d * "x", lambda: d / "x",  # type: ignore[operator]
                lambda: d < "x", lambda: d <= "x",  # type: ignore[operator]
                lambda: d > "x", lambda: d >= "x",  # type: ignore[operator]
            ]
            for attempt in attempts:
                try:
                    attempt()
                except TypeError:
                    continue
                return False  # an operator accepted a foreign operand
            return True
        return super().condition(feature, *args, **kwargs)


class RejectsForeignOperandsMixin(RejectsForeignOperandsMixinBase, ABC):
    negative_rejects_foreign_operands: bool = False

    @pytest.mark.feature_duration_operators
    def test_rejects_foreign_operands(self) -> None:
        """All operators raise TypeError for unsupported operand types."""
        assert self.validate("rejects_foreign_operands")


class NoRejectsForeignOperandsMixin(RejectsForeignOperandsMixinBase, ABC):
    negative_rejects_foreign_operands: bool = True

    @pytest.mark.feature_duration_operators
    def test_rejects_foreign_operands(self) -> None:
        """Negated variant: some operator must accept foreign operands."""
        assert self.validate("rejects_foreign_operands")


# ------------------------------------------------------------------ comparison
class ComparesByValueMixinBase(Mixin, ABC):
    """Feature: ==/hash compare by simplified value across representations."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "compares_by_value":
            return (
                Duration(seconds=90) == Duration(seconds=90)  # fast path
                and Duration(seconds=90) == Duration(minutes=1, seconds=30)  # slow path
                and Duration(seconds=90) != Duration(seconds=91)
                and Duration(seconds=90) != "90"  # foreign type, no error
                and hash(Duration(seconds=90)) == hash(Duration(minutes=1, seconds=30))
            )
        return super().condition(feature, *args, **kwargs)


class ComparesByValueMixin(ComparesByValueMixinBase, ABC):
    negative_compares_by_value: bool = False

    @pytest.mark.feature_duration_compare
    @pytest.mark.feature_equality
    def test_compares_by_value(self) -> None:
        """Equal values in different unit mixes compare and hash equal."""
        assert self.validate("compares_by_value")


class NoComparesByValueMixin(ComparesByValueMixinBase, ABC):
    negative_compares_by_value: bool = True

    @pytest.mark.feature_duration_compare
    @pytest.mark.feature_equality
    def test_compares_by_value(self) -> None:
        """Negated variant: value equality must not hold."""
        assert self.validate("compares_by_value")


class OrdersChronologicallyMixinBase(Mixin, ABC):
    """Feature: <, <=, >, >= order durations against all supported types,
    and truthiness reflects non-zero length."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "orders_chronologically":
            return (
                Duration(seconds=30) < Duration(minutes=1)
                and Duration(seconds=60) <= timedelta(minutes=1)
                and Duration(minutes=2) > 100
                and Duration(minutes=1) >= 60
                and not Duration(minutes=1) < 60
                and bool(Duration(seconds=1))
                and not bool(Duration())
            )
        return super().condition(feature, *args, **kwargs)


class OrdersChronologicallyMixin(OrdersChronologicallyMixinBase, ABC):
    negative_orders_chronologically: bool = False

    @pytest.mark.feature_duration_compare
    def test_orders_chronologically(self) -> None:
        """Rich comparisons and truthiness follow total length."""
        assert self.validate("orders_chronologically")


class NoOrdersChronologicallyMixin(OrdersChronologicallyMixinBase, ABC):
    negative_orders_chronologically: bool = True

    @pytest.mark.feature_duration_compare
    def test_orders_chronologically(self) -> None:
        """Negated variant: ordering must not follow total length."""
        assert self.validate("orders_chronologically")


# ---------------------------------------------------------------- test classes
class DurationCoreMixins(
    BuildsFromOtherFormsMixin,
    NoFailsCreateFromUnsupportedMixin,
    SimplifiesUnitsMixin,
    ReportsSimplifiedStateMixin,
    ComputesTotalSecondsMixin,
    AddsAndSubtractsMixin,
    ScalesAndDividesMixin,
    HandlesSignsMixin,
    RejectsForeignOperandsMixin,
    ComparesByValueMixin,
    OrdersChronologicallyMixin,
    ABC,
):
    """Group: the full Duration contract (day-free windows only; see module
    docstring for why day-based totals are excluded)."""


class TestDuration(DurationCoreMixins):
    """Duration satisfies its construction/simplify/operator contracts."""


class TestTotalSecondsRejectsWeekdays(NoFailsTotalSecondsOnInexactUnitsMixin):
    """Method-focused: total_seconds() guards against weekday units."""

    @pytest.fixture
    def inexact_duration(self) -> Duration:
        return Duration(weekdays=1)


class TestTotalSecondsRejectsMonths(NoFailsTotalSecondsOnInexactUnitsMixin):
    """Method-focused: total_seconds() guards against unfixed months."""

    @pytest.fixture
    def inexact_duration(self) -> Duration:
        return Duration(months=1)


class TestTotalSecondsRejectsYears(NoFailsTotalSecondsOnInexactUnitsMixin):
    """Method-focused: total_seconds() guards against unfixed years."""

    @pytest.fixture
    def inexact_duration(self) -> Duration:
        return Duration(years=1)
