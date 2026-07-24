"""
Tests for datecomponents/duration.py.

Durations built from days are excluded from any total_seconds assertions
because of defect D5 (days are converted at 8640 s/day instead of 86400; see
REPORT.md and tests/test_rejections.py). Weeks, hours, minutes and seconds all
convert correctly and are used instead. Structural behavior (simplify,
equality, field storage) is unaffected by D5 and fully tested.
"""
from abc import ABC
from datetime import timedelta
from typing import Any

import pytest

from datecomponents.duration import Duration
from tests.test_utils import Mixin


# --- feature: defaults_to_zero ------------------------------------------------

class DefaultsToZeroMixinBase(Mixin, ABC):
    """A bare Duration() is the zero duration."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "defaults_to_zero":
            zero = Duration()
            return zero.total_seconds() == 0 and not bool(zero)
        return super().condition(feature, *args, **kwargs)


class DefaultsToZeroMixin(DefaultsToZeroMixinBase, ABC):
    negative_defaults_to_zero: bool = False

    @pytest.mark.construction
    def test_defaults_to_zero(self) -> None:
        """All units default to 0, making the default instance falsy."""
        assert self.validate("defaults_to_zero")


class NoDefaultsToZeroMixin(DefaultsToZeroMixin, ABC):
    negative_defaults_to_zero: bool = True


# --- feature: builds_from_alternate_sources (classmethods) ---------------------

class BuildsFromAlternateSourcesMixinBase(Mixin, ABC):
    """from_seconds / from_timedelta / create_from construction paths."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "builds_from_alternate_sources":
            td = timedelta(days=2, seconds=30, microseconds=500_000)
            existing = Duration(minutes=1)
            return (
                # from_seconds stores into the seconds field (fast-path __eq__).
                Duration.from_seconds(90) == Duration(seconds=90)
                # from_timedelta keeps days/seconds structure (incl. microseconds).
                and Duration.from_timedelta(td) == Duration(days=2, seconds=30.5)
                # create_from: passthrough, timedelta and number dispatch.
                and Duration.create_from(existing) is existing
                and Duration.create_from(td) == Duration.from_timedelta(td)
                and Duration.create_from(90) == Duration(seconds=90)
                and Duration.create_from(1.5) == Duration(seconds=1.5)
            )
        return super().condition(feature, *args, **kwargs)


class BuildsFromAlternateSourcesMixin(BuildsFromAlternateSourcesMixinBase, ABC):
    negative_builds_from_alternate_sources: bool = False

    @pytest.mark.construction
    @pytest.mark.static
    def test_builds_from_alternate_sources(self) -> None:
        """The three classmethod constructors agree with direct construction."""
        assert self.validate("builds_from_alternate_sources")


class NoBuildsFromAlternateSourcesMixin(BuildsFromAlternateSourcesMixin, ABC):
    negative_builds_from_alternate_sources: bool = True


# --- feature: fails_create_from_bad_type (classmethod) --------------------------

class FailsCreateFromBadTypeMixinBase(Mixin, ABC):
    """create_from rejects unsupported source types."""

    fail_fails_create_from_bad_type: type[BaseException] = TypeError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_create_from_bad_type":
            Duration.create_from("ninety")  # type: ignore[arg-type]
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsCreateFromBadTypeMixin(FailsCreateFromBadTypeMixinBase, ABC):
    negative_fails_create_from_bad_type: bool = False

    @pytest.mark.construction
    @pytest.mark.static
    def test_fails_create_from_bad_type(self) -> None:
        """create_from(str) raises TypeError (asserted inside validate)."""
        self.validate("fails_create_from_bad_type")


class NoFailsCreateFromBadTypeMixin(FailsCreateFromBadTypeMixin, ABC):
    negative_fails_create_from_bad_type: bool = True


# --- feature: totals_exact_units -------------------------------------------------

class TotalsExactUnitsMixinBase(Mixin, ABC):
    """total_seconds/to_timedelta for the units with correct conversions."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "totals_exact_units":
            return (
                Duration(hours=2, minutes=30, seconds=15).total_seconds() == 9015
                and Duration(weeks=2).total_seconds() == 1_209_600
                and Duration(seconds=5400).to_timedelta()
                == timedelta(hours=1, minutes=30)
            )
        return super().condition(feature, *args, **kwargs)


class TotalsExactUnitsMixin(TotalsExactUnitsMixinBase, ABC):
    negative_totals_exact_units: bool = False

    @pytest.mark.conversion
    def test_totals_exact_units(self) -> None:
        """Seconds/minutes/hours/weeks produce correct totals and timedeltas."""
        assert self.validate("totals_exact_units")


class NoTotalsExactUnitsMixin(TotalsExactUnitsMixin, ABC):
    negative_totals_exact_units: bool = True


# --- feature: fails_total_with_inexact_units --------------------------------------

class FailsTotalWithInexactUnitsMixinBase(Mixin, ABC):
    """weekdays/months/years have no fixed length -> total_seconds raises."""

    fail_fails_total_with_inexact_units: type[BaseException] = ValueError

    @pytest.fixture
    def inexact_duration(self) -> Duration:
        """A Duration containing at least one unit with no fixed length."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_total_with_inexact_units":
            inexact: Duration = kwargs["inexact_duration"]
            inexact.total_seconds()
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsTotalWithInexactUnitsMixin(FailsTotalWithInexactUnitsMixinBase, ABC):
    negative_fails_total_with_inexact_units: bool = False

    @pytest.mark.conversion
    def test_fails_total_with_weekdays(self) -> None:
        """Weekdays never have a fixed length, so totals are refused."""
        self.validate(
            "fails_total_with_inexact_units",
            inexact_duration=Duration(weekdays=1),
        )

    @pytest.mark.conversion
    def test_fails_total_with_months(self) -> None:
        """Months are refused unless month_days pins their length."""
        self.validate(
            "fails_total_with_inexact_units",
            inexact_duration=Duration(months=1),
        )

    @pytest.mark.conversion
    def test_fails_total_with_years(self) -> None:
        """Years are refused unless year_days pins their length."""
        self.validate(
            "fails_total_with_inexact_units",
            inexact_duration=Duration(years=1),
        )


class NoFailsTotalWithInexactUnitsMixin(FailsTotalWithInexactUnitsMixin, ABC):
    negative_fails_total_with_inexact_units: bool = True


# --- feature: pinned_lengths_make_units_exact ---------------------------------------

class PinnedLengthsMakeUnitsExactMixinBase(Mixin, ABC):
    """month_days/year_days fold months/years into exact day counts."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "pinned_lengths_make_units_exact":
            # 28 and 364 are whole numbers of weeks, dodging defect D5 so the
            # fold itself can be asserted against correct second counts.
            month = Duration(months=1, month_days=28)
            year = Duration(years=1, year_days=364)
            return (
                month.total_seconds() == 28 * 86_400
                and year.total_seconds() == 364 * 86_400
                and month.simplify().months == 0  # folded away
                and year.simplify().years == 0
            )
        return super().condition(feature, *args, **kwargs)


class PinnedLengthsMakeUnitsExactMixin(PinnedLengthsMakeUnitsExactMixinBase, ABC):
    negative_pinned_lengths_make_units_exact: bool = False

    @pytest.mark.simplification
    def test_pinned_lengths_make_units_exact(self) -> None:
        """Setting month_days/year_days converts months/years into real spans."""
        assert self.validate("pinned_lengths_make_units_exact")


class NoPinnedLengthsMakeUnitsExactMixin(PinnedLengthsMakeUnitsExactMixin, ABC):
    negative_pinned_lengths_make_units_exact: bool = True


# --- feature: simplifies_units --------------------------------------------------------

class SimplifiesUnitsMixinBase(Mixin, ABC):
    """simplify() cascades fractions down and normalizes whole units up."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "simplifies_units":
            upward = Duration(seconds=3725).simplify()
            fractional = Duration(days=1.5).simplify()
            return (
                (upward.hours, upward.minutes, upward.seconds) == (1, 2, 5)
                and (fractional.days, fractional.hours) == (1, 12)
            )
        return super().condition(feature, *args, **kwargs)


class SimplifiesUnitsMixin(SimplifiesUnitsMixinBase, ABC):
    negative_simplifies_units: bool = False

    @pytest.mark.simplification
    def test_simplifies_units(self) -> None:
        """3725s -> 1h 2m 5s; 1.5 days -> 1 day 12 hours."""
        assert self.validate("simplifies_units")


class NoSimplifiesUnitsMixin(SimplifiesUnitsMixin, ABC):
    negative_simplifies_units: bool = True


# --- feature: simplify_is_idempotent ----------------------------------------------------

class SimplifyIsIdempotentMixinBase(Mixin, ABC):
    """Simplifying twice changes nothing and is_simplified flags the state."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "simplify_is_idempotent":
            raw = Duration(seconds=90)
            simplified = raw.simplify()
            return (
                not raw.is_simplified()
                and simplified.is_simplified()
                # Repeated calls are deterministic (also exercises the cache).
                and raw.simplify() == simplified
            )
        return super().condition(feature, *args, **kwargs)


class SimplifyIsIdempotentMixin(SimplifyIsIdempotentMixinBase, ABC):
    negative_simplify_is_idempotent: bool = False

    @pytest.mark.simplification
    def test_simplify_is_idempotent(self) -> None:
        """is_simplified() distinguishes raw from reduced forms; simplify is stable."""
        assert self.validate("simplify_is_idempotent")


class NoSimplifyIsIdempotentMixin(SimplifyIsIdempotentMixin, ABC):
    negative_simplify_is_idempotent: bool = True


# --- feature: equal_across_unit_mixes ------------------------------------------------------

class EqualAcrossUnitMixesMixinBase(Mixin, ABC):
    """Equality and hashing are based on the simplified representation."""

    @pytest.fixture
    def equal_left(self) -> Duration:
        """One spelling of the span."""
        raise NotImplementedError

    @pytest.fixture
    def equal_right(self) -> Duration:
        """A differently spelled but equivalent span."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "equal_across_unit_mixes":
            left: Duration = kwargs["equal_left"]
            right: Duration = kwargs["equal_right"]
            return left == right and hash(left) == hash(right)
        return super().condition(feature, *args, **kwargs)


class EqualAcrossUnitMixesMixin(EqualAcrossUnitMixesMixinBase, ABC):
    negative_equal_across_unit_mixes: bool = False

    @pytest.mark.identity
    def test_equal_across_unit_mixes(
        self, equal_left: Duration, equal_right: Duration
    ) -> None:
        """1 minute equals 60 seconds, including their hashes."""
        assert self.validate(
            "equal_across_unit_mixes", equal_left=equal_left, equal_right=equal_right
        )


class NoEqualAcrossUnitMixesMixin(EqualAcrossUnitMixesMixin, ABC):
    negative_equal_across_unit_mixes: bool = True


# --- feature: equal_to_non_duration -----------------------------------------------------------

class EqualToNonDurationMixinBase(Mixin, ABC):
    """__eq__ returns NotImplemented for foreign types -> `==` is False."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "equal_to_non_duration":
            return Duration(seconds=60) == 60  # plain numbers are not Durations
        return super().condition(feature, *args, **kwargs)


class EqualToNonDurationMixin(EqualToNonDurationMixinBase, ABC):
    negative_equal_to_non_duration: bool = False

    @pytest.mark.identity
    def test_equal_to_non_duration(self) -> None:
        """A Duration never equals a bare number (used via the No variant)."""
        assert self.validate("equal_to_non_duration")


class NoEqualToNonDurationMixin(EqualToNonDurationMixin, ABC):
    negative_equal_to_non_duration: bool = True


# --- feature: adds_and_subtracts ---------------------------------------------------------------

class AddsAndSubtractsMixinBase(Mixin, ABC):
    """+/- accept Durations, timedeltas and numbers on either side."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "adds_and_subtracts":
            minute = Duration(minutes=1)
            ninety = Duration(seconds=90)
            return (
                minute + Duration(seconds=30) == ninety
                and minute + timedelta(seconds=30) == ninety
                and minute + 30 == ninety
                and 30 + minute == ninety  # __radd__
                and timedelta(seconds=30) + minute == ninety  # __radd__
                and Duration(minutes=2) - Duration(seconds=30) == ninety
                and Duration(minutes=2) - 30 == ninety
                and 120 - Duration(seconds=30) == ninety  # __rsub__
                and timedelta(seconds=120) - Duration(seconds=30) == ninety
            )
        return super().condition(feature, *args, **kwargs)


class AddsAndSubtractsMixin(AddsAndSubtractsMixinBase, ABC):
    negative_adds_and_subtracts: bool = False

    @pytest.mark.arithmetic
    def test_adds_and_subtracts(self) -> None:
        """Addition/subtraction inter-operate with timedelta and numbers."""
        assert self.validate("adds_and_subtracts")


class NoAddsAndSubtractsMixin(AddsAndSubtractsMixin, ABC):
    negative_adds_and_subtracts: bool = True


# --- feature: add_preserves_pinned_lengths ------------------------------------------------------

class AddPreservesPinnedLengthsMixinBase(Mixin, ABC):
    """Adding keeps month_days/year_days from whichever operand sets them."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "add_preserves_pinned_lengths":
            pinned_year = Duration(years=1, year_days=364)
            pinned_month = Duration(months=1, month_days=28)
            week = Duration(weeks=1)
            # Note: `==` cannot be used against an unpinned Duration(weeks=53)
            # because the pin itself participates in equality (see REPORT.md,
            # concern C2), so the structure and totals are asserted instead.
            return (
                (pinned_year + week).weeks == 53
                and (week + pinned_year).weeks == 53  # right side pins
                and (pinned_month + week).weeks == 5
                and (pinned_year + week).year_days == 364
                and (pinned_year + week).total_seconds() == 53 * 604_800
            )
        return super().condition(feature, *args, **kwargs)


class AddPreservesPinnedLengthsMixin(AddPreservesPinnedLengthsMixinBase, ABC):
    negative_add_preserves_pinned_lengths: bool = False

    @pytest.mark.arithmetic
    @pytest.mark.simplification
    def test_add_preserves_pinned_lengths(self) -> None:
        """Pinned month/year lengths survive addition from either operand."""
        assert self.validate("add_preserves_pinned_lengths")


class NoAddPreservesPinnedLengthsMixin(AddPreservesPinnedLengthsMixin, ABC):
    negative_add_preserves_pinned_lengths: bool = True


# --- feature: scales_by_scalar -------------------------------------------------------------------

class ScalesByScalarMixinBase(Mixin, ABC):
    """* and / with numbers scale the duration; / with spans gives a ratio."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "scales_by_scalar":
            two_minutes = Duration(minutes=2)
            return (
                two_minutes * 3 == Duration(minutes=6)
                and 3 * two_minutes == Duration(minutes=6)  # __rmul__
                and two_minutes / 2 == Duration(minutes=1)
                and two_minutes / Duration(seconds=60) == 2.0
                and two_minutes / timedelta(seconds=60) == 2.0
            )
        return super().condition(feature, *args, **kwargs)


class ScalesByScalarMixin(ScalesByScalarMixinBase, ABC):
    negative_scales_by_scalar: bool = False

    @pytest.mark.arithmetic
    def test_scales_by_scalar(self) -> None:
        """Multiplication/division by numbers and division by spans work."""
        assert self.validate("scales_by_scalar")


class NoScalesByScalarMixin(ScalesByScalarMixin, ABC):
    negative_scales_by_scalar: bool = True


# --- feature: signs_and_truthiness ----------------------------------------------------------------

class SignsAndTruthinessMixinBase(Mixin, ABC):
    """-, abs(), +, and bool() follow the numeric protocol for exact spans."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "signs_and_truthiness":
            # Week-granular values are used because negative spans that
            # borrow through the days place are corrupted by defect D5.
            week = Duration(weeks=1)
            negative_week = Duration(weeks=-1)
            return (
                -week == negative_week
                and abs(negative_week) == week
                and abs(week) == week  # already positive: unchanged
                and +week is week
                and bool(week)
                and not bool(Duration())
            )
        return super().condition(feature, *args, **kwargs)


class SignsAndTruthinessMixin(SignsAndTruthinessMixinBase, ABC):
    negative_signs_and_truthiness: bool = False

    @pytest.mark.arithmetic
    def test_signs_and_truthiness(self) -> None:
        """Negation, absolute value, unary plus and truthiness behave numerically."""
        assert self.validate("signs_and_truthiness")


class NoSignsAndTruthinessMixin(SignsAndTruthinessMixin, ABC):
    negative_signs_and_truthiness: bool = True


# --- feature: orders_by_total_seconds --------------------------------------------------------------

class OrdersByTotalSecondsMixinBase(Mixin, ABC):
    """<, <=, >, >= compare spans across Duration/timedelta/number operands."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "orders_by_total_seconds":
            one = Duration(minutes=1)
            two = Duration(minutes=2)
            return (
                one < two
                and one <= Duration(seconds=60)
                and two > timedelta(seconds=90)
                and two >= 120
            )
        return super().condition(feature, *args, **kwargs)


class OrdersByTotalSecondsMixin(OrdersByTotalSecondsMixinBase, ABC):
    negative_orders_by_total_seconds: bool = False

    @pytest.mark.comparison
    def test_orders_by_total_seconds(self) -> None:
        """All four ordering operators respect the total span length."""
        assert self.validate("orders_by_total_seconds")


class NoOrdersByTotalSecondsMixin(OrdersByTotalSecondsMixin, ABC):
    negative_orders_by_total_seconds: bool = True


# --- feature: fails_operator_with_bad_operand -------------------------------------------------------

class FailsOperatorWithBadOperandMixinBase(Mixin, ABC):
    """Every operator returns NotImplemented for foreign types -> TypeError."""

    fail_fails_operator_with_bad_operand: type[BaseException] = TypeError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_operator_with_bad_operand":
            op: str = kwargs["op"]
            d = Duration(seconds=1)
            # Each branch evaluates exactly one operator against a string,
            # which must bubble up as TypeError via NotImplemented.
            expressions = {
                "add": lambda: d + "x",
                "radd": lambda: "x" + d,
                "sub": lambda: d - "x",
                "rsub": lambda: "x" - d,
                "mul": lambda: d * "x",
                "div": lambda: d / "x",
                "lt": lambda: d < "x",
                "le": lambda: d <= "x",
                "gt": lambda: d > "x",
                "ge": lambda: d >= "x",
            }
            expressions[op]()  # type: ignore[operator]
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsOperatorWithBadOperandMixin(FailsOperatorWithBadOperandMixinBase, ABC):
    negative_fails_operator_with_bad_operand: bool = False

    # One test per operator keeps each failure independent and reportable.
    @pytest.mark.arithmetic
    def test_fails_add_with_bad_operand(self) -> None:
        """d + str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="add")

    @pytest.mark.arithmetic
    def test_fails_radd_with_bad_operand(self) -> None:
        """str + d raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="radd")

    @pytest.mark.arithmetic
    def test_fails_sub_with_bad_operand(self) -> None:
        """d - str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="sub")

    @pytest.mark.arithmetic
    def test_fails_rsub_with_bad_operand(self) -> None:
        """str - d raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="rsub")

    @pytest.mark.arithmetic
    def test_fails_mul_with_bad_operand(self) -> None:
        """d * str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="mul")

    @pytest.mark.arithmetic
    def test_fails_div_with_bad_operand(self) -> None:
        """d / str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="div")

    @pytest.mark.comparison
    def test_fails_lt_with_bad_operand(self) -> None:
        """d < str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="lt")

    @pytest.mark.comparison
    def test_fails_le_with_bad_operand(self) -> None:
        """d <= str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="le")

    @pytest.mark.comparison
    def test_fails_gt_with_bad_operand(self) -> None:
        """d > str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="gt")

    @pytest.mark.comparison
    def test_fails_ge_with_bad_operand(self) -> None:
        """d >= str raises TypeError."""
        self.validate("fails_operator_with_bad_operand", op="ge")


class NoFailsOperatorWithBadOperandMixin(FailsOperatorWithBadOperandMixin, ABC):
    negative_fails_operator_with_bad_operand: bool = True


# --- feature: fails_scaling_inexact_units ------------------------------------------------------------

class FailsScalingInexactUnitsMixinBase(Mixin, ABC):
    """
    Current (deliberate, if debatable - see REPORT.md, concern C3) behavior:
    * and / refuse durations containing months/years/weekdays.
    """

    fail_fails_scaling_inexact_units: type[BaseException] = ValueError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_scaling_inexact_units":
            Duration(months=1) * 2
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsScalingInexactUnitsMixin(FailsScalingInexactUnitsMixinBase, ABC):
    negative_fails_scaling_inexact_units: bool = False

    @pytest.mark.arithmetic
    def test_fails_scaling_inexact_units(self) -> None:
        """Multiplying a month-bearing duration raises ValueError today."""
        self.validate("fails_scaling_inexact_units")


class NoFailsScalingInexactUnitsMixin(FailsScalingInexactUnitsMixin, ABC):
    negative_fails_scaling_inexact_units: bool = True


# =====================================================================================
# Test classes
# =====================================================================================

class TestDuration(
    DefaultsToZeroMixin,
    BuildsFromAlternateSourcesMixin,
    FailsCreateFromBadTypeMixin,
    TotalsExactUnitsMixin,
    FailsTotalWithInexactUnitsMixin,
    PinnedLengthsMakeUnitsExactMixin,
    SimplifiesUnitsMixin,
    SimplifyIsIdempotentMixin,
    EqualAcrossUnitMixesMixin,
    NoEqualToNonDurationMixin,
    AddsAndSubtractsMixin,
    AddPreservesPinnedLengthsMixin,
    ScalesByScalarMixin,
    SignsAndTruthinessMixin,
    OrdersByTotalSecondsMixin,
    FailsOperatorWithBadOperandMixin,
    FailsScalingInexactUnitsMixin,
):
    """Full Duration feature suite with an equivalent-spans equality pair."""

    @pytest.fixture
    def equal_left(self) -> Duration:
        return Duration(minutes=1)

    @pytest.fixture
    def equal_right(self) -> Duration:
        # Same span spelled in seconds: forces the slow (simplified) eq path.
        return Duration(seconds=60)


class TestDurationUnequalSpans(NoEqualAcrossUnitMixesMixin):
    """
    The inherited equality test re-run on spans that must NOT be equal,
    via the negated variant of the same feature.
    """

    @pytest.fixture
    def equal_left(self) -> Duration:
        return Duration(seconds=60)

    @pytest.fixture
    def equal_right(self) -> Duration:
        # One second longer: both the fast and slow eq paths reject it,
        # and the hashes differ.
        return Duration(seconds=61)
