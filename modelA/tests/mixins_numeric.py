"""
Feature mixins for `NumericDateComponentBase` behavior.

Each feature follows the standard three-class layout:
`...MixinBase` (condition + abstract fixtures), `...Mixin` (positive) and
`No...Mixin` (negated). Feature strings are derived from the base-class name.

Exception-based features use the `Fails...` naming convention and set a
`fail_<feature>` attribute; per the `Mixin.validate` contract the condition
result then stays False, so those features are consumed through their
`No...Mixin` (negative=True) variant to make the assertion pass.
"""
import pytest
from abc import ABC, abstractmethod
from typing import Any

from test_utils import Mixin
from dateutils.base import NumericDateComponentBase


# ---------------------------------------------------------------- construction
class ConstructsFromIntMixinBase(Mixin, ABC):
    """Feature: a component can be built from an in-range int and converts back."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]:
        """The public component class under test."""

    @pytest.fixture
    @abstractmethod
    def in_range_value(self) -> int:
        """Any int strictly inside the component's valid range."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "constructs_from_int":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            value: int = kwargs["in_range_value"]
            obj = cls(value)
            # int_id round-trips and __int__ mirrors it.
            return obj.int_id == value and int(obj) == value
        return super().condition(feature, *args, **kwargs)


class ConstructsFromIntMixin(ConstructsFromIntMixinBase, ABC):
    negative_constructs_from_int: bool = False

    @pytest.mark.feature_construction
    def test_constructs_from_int(self, component_cls: type[NumericDateComponentBase], in_range_value: int) -> None:
        """In-range ints are stored verbatim and exposed via int_id/__int__."""
        assert self.validate("constructs_from_int", component_cls=component_cls, in_range_value=in_range_value)


class NoConstructsFromIntMixin(ConstructsFromIntMixinBase, ABC):
    negative_constructs_from_int: bool = True

    @pytest.mark.feature_construction
    def test_constructs_from_int(self, component_cls: type[NumericDateComponentBase], in_range_value: int) -> None:
        """Negated variant: int construction must NOT round-trip."""
        assert self.validate("constructs_from_int", component_cls=component_cls, in_range_value=in_range_value)


# --------------------------------------------------------------- normalization
class ClampsOutOfRangeIntsMixinBase(Mixin, ABC):
    """Feature: out-of-range ints are silently clamped (documented behavior),
    both at construction time and through the int_id setter."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def min_value(self) -> int:
        """The smallest valid int for the component."""

    @pytest.fixture
    @abstractmethod
    def max_value(self) -> int:
        """The largest valid int for the component."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "clamps_out_of_range_ints":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            lo: int = kwargs["min_value"]
            hi: int = kwargs["max_value"]
            above = cls(hi + 100)
            below = cls(lo - 100)
            # Re-assignment through the property setter must clamp too.
            above.int_id = lo - 100
            return below.int_id == lo and above.int_id == lo and cls(hi + 1).int_id == hi
        return super().condition(feature, *args, **kwargs)


class ClampsOutOfRangeIntsMixin(ClampsOutOfRangeIntsMixinBase, ABC):
    negative_clamps_out_of_range_ints: bool = False

    @pytest.mark.feature_normalization
    def test_clamps_out_of_range_ints(self, component_cls: type[NumericDateComponentBase], min_value: int, max_value: int) -> None:
        """Out-of-range ints clamp to the documented [min, max] bounds."""
        assert self.validate("clamps_out_of_range_ints", component_cls=component_cls, min_value=min_value, max_value=max_value)


class NoClampsOutOfRangeIntsMixin(ClampsOutOfRangeIntsMixinBase, ABC):
    negative_clamps_out_of_range_ints: bool = True

    @pytest.mark.feature_normalization
    def test_clamps_out_of_range_ints(self, component_cls: type[NumericDateComponentBase], min_value: int, max_value: int) -> None:
        """Negated variant: clamping must NOT occur."""
        assert self.validate("clamps_out_of_range_ints", component_cls=component_cls, min_value=min_value, max_value=max_value)


class NormalizesIntsStaticallyMixinBase(Mixin, ABC):
    """Feature: normalize_int is usable directly on the class (static test)."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def max_value(self) -> int: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "normalizes_ints_statically":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            hi: int = kwargs["max_value"]
            return cls.normalize_int(hi + 3) == hi and cls.normalize_int(hi) == hi
        return super().condition(feature, *args, **kwargs)


class NormalizesIntsStaticallyMixin(NormalizesIntsStaticallyMixinBase, ABC):
    negative_normalizes_ints_statically: bool = False

    @pytest.mark.feature_normalization
    @pytest.mark.static
    def test_normalizes_ints_statically(self, component_cls: type[NumericDateComponentBase], max_value: int) -> None:
        """normalize_int clamps without requiring an instance."""
        assert self.validate("normalizes_ints_statically", component_cls=component_cls, max_value=max_value)


class NoNormalizesIntsStaticallyMixin(NormalizesIntsStaticallyMixinBase, ABC):
    negative_normalizes_ints_statically: bool = True

    @pytest.mark.feature_normalization
    @pytest.mark.static
    def test_normalizes_ints_statically(self, component_cls: type[NumericDateComponentBase], max_value: int) -> None:
        """Negated variant: class-level normalization must NOT clamp."""
        assert self.validate("normalizes_ints_statically", component_cls=component_cls, max_value=max_value)


class FailsOnBoolConstructionMixinBase(Mixin, ABC):
    """Feature: bools are deliberately excluded from the int fast-path
    (`type(value) is int`), so constructing from a bool raises TypeError."""

    fail_fails_on_bool_construction: type[BaseException] = TypeError

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_on_bool_construction":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            cls(True)  # type: ignore[arg-type]  # deliberate misuse
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsOnBoolConstructionMixin(FailsOnBoolConstructionMixinBase, ABC):
    negative_fails_on_bool_construction: bool = False

    @pytest.mark.feature_normalization
    def test_fails_on_bool_construction(self, component_cls: type[NumericDateComponentBase]) -> None:
        """Positive variant (unused in practice; see NoFailsOnBoolConstructionMixin)."""
        assert self.validate("fails_on_bool_construction", component_cls=component_cls)


class NoFailsOnBoolConstructionMixin(FailsOnBoolConstructionMixinBase, ABC):
    # With fail_* set, the condition raises inside pytest.raises and the result
    # stays False; negating yields True, so this is the asserting variant.
    negative_fails_on_bool_construction: bool = True

    @pytest.mark.feature_normalization
    def test_fails_on_bool_construction(self, component_cls: type[NumericDateComponentBase]) -> None:
        """Constructing from a bool raises TypeError (bools are not ints here)."""
        assert self.validate("fails_on_bool_construction", component_cls=component_cls)


class RejectsStringValuesMixinBase(Mixin, ABC):
    """Feature: plain numeric components reject string inputs with TypeError.
    Named subclasses legitimately accept strings, so they negate this feature."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def sample_name(self) -> str:
        """A string; a valid name for named components, arbitrary otherwise."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "rejects_string_values":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            try:
                cls(kwargs["sample_name"])  # type: ignore[arg-type]
            except TypeError:
                return True
            return False
        return super().condition(feature, *args, **kwargs)


class RejectsStringValuesMixin(RejectsStringValuesMixinBase, ABC):
    negative_rejects_string_values: bool = False

    @pytest.mark.feature_normalization
    def test_rejects_string_values(self, component_cls: type[NumericDateComponentBase], sample_name: str) -> None:
        """Plain numeric components raise TypeError for any string input."""
        assert self.validate("rejects_string_values", component_cls=component_cls, sample_name=sample_name)


class NoRejectsStringValuesMixin(RejectsStringValuesMixinBase, ABC):
    negative_rejects_string_values: bool = True

    @pytest.mark.feature_normalization
    def test_rejects_string_values(self, component_cls: type[NumericDateComponentBase], sample_name: str) -> None:
        """Negated variant: string input must be accepted (named components)."""
        assert self.validate("rejects_string_values", component_cls=component_cls, sample_name=sample_name)


# -------------------------------------------------------------------- equality
class ComparesByIntIdMixinBase(Mixin, ABC):
    """Feature: equality/hash are driven by int_id; other types compare unequal
    (not erroring), and equal objects hash identically."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def in_range_value(self) -> int: ...

    @pytest.fixture
    @abstractmethod
    def other_in_range_value(self) -> int:
        """A second, different in-range int."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "compares_by_int_id":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            a, b = kwargs["in_range_value"], kwargs["other_in_range_value"]
            return (
                cls(a) == cls(a)
                and cls(a) != cls(b)
                and cls(a) != a  # plain ints are not components
                and hash(cls(a)) == hash(cls(a))
            )
        return super().condition(feature, *args, **kwargs)


class ComparesByIntIdMixin(ComparesByIntIdMixinBase, ABC):
    negative_compares_by_int_id: bool = False

    @pytest.mark.feature_equality
    def test_compares_by_int_id(self, component_cls: type[NumericDateComponentBase], in_range_value: int, other_in_range_value: int) -> None:
        """Same-type/same-value equality, inequality otherwise, stable hash."""
        assert self.validate("compares_by_int_id", component_cls=component_cls, in_range_value=in_range_value, other_in_range_value=other_in_range_value)


class NoComparesByIntIdMixin(ComparesByIntIdMixinBase, ABC):
    negative_compares_by_int_id: bool = True

    @pytest.mark.feature_equality
    def test_compares_by_int_id(self, component_cls: type[NumericDateComponentBase], in_range_value: int, other_in_range_value: int) -> None:
        """Negated variant: equality must not be purely int_id-driven."""
        assert self.validate("compares_by_int_id", component_cls=component_cls, in_range_value=in_range_value, other_in_range_value=other_in_range_value)


# ----------------------------------------------------------------- create_from
class CopiesViaCreateFromMixinBase(Mixin, ABC):
    """Feature: create_from accepts an int or an existing instance and always
    returns an equal but distinct instance (static test)."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def in_range_value(self) -> int: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "copies_via_create_from":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            value: int = kwargs["in_range_value"]
            original = cls(value)
            copy = cls.create_from(original)
            return (
                cls.create_from(value).int_id == value
                and copy.int_id == original.int_id
                and copy is not original
            )
        return super().condition(feature, *args, **kwargs)


class CopiesViaCreateFromMixin(CopiesViaCreateFromMixinBase, ABC):
    negative_copies_via_create_from: bool = False

    @pytest.mark.feature_construction
    @pytest.mark.static
    def test_copies_via_create_from(self, component_cls: type[NumericDateComponentBase], in_range_value: int) -> None:
        """create_from builds from ints and copies instances (distinct object)."""
        assert self.validate("copies_via_create_from", component_cls=component_cls, in_range_value=in_range_value)


class NoCopiesViaCreateFromMixin(CopiesViaCreateFromMixinBase, ABC):
    negative_copies_via_create_from: bool = True

    @pytest.mark.feature_construction
    @pytest.mark.static
    def test_copies_via_create_from(self, component_cls: type[NumericDateComponentBase], in_range_value: int) -> None:
        """Negated variant: create_from must not copy faithfully."""
        assert self.validate("copies_via_create_from", component_cls=component_cls, in_range_value=in_range_value)


# -------------------------------------------------------------------- argparse
class ParsesArgtypeIntsMixinBase(Mixin, ABC):
    """Feature: argtype parses numeric strings and clamps them (static test)."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def in_range_value(self) -> int: ...

    @pytest.fixture
    @abstractmethod
    def max_value(self) -> int: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "parses_argtype_ints":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            value: int = kwargs["in_range_value"]
            hi: int = kwargs["max_value"]
            return cls.argtype(str(value)) == value and cls.argtype(str(hi + 500)) == hi
        return super().condition(feature, *args, **kwargs)


class ParsesArgtypeIntsMixin(ParsesArgtypeIntsMixinBase, ABC):
    negative_parses_argtype_ints: bool = False

    @pytest.mark.feature_argparse
    @pytest.mark.static
    def test_parses_argtype_ints(self, component_cls: type[NumericDateComponentBase], in_range_value: int, max_value: int) -> None:
        """argtype converts numeric CLI strings to clamped ints."""
        assert self.validate("parses_argtype_ints", component_cls=component_cls, in_range_value=in_range_value, max_value=max_value)


class NoParsesArgtypeIntsMixin(ParsesArgtypeIntsMixinBase, ABC):
    negative_parses_argtype_ints: bool = True

    @pytest.mark.feature_argparse
    @pytest.mark.static
    def test_parses_argtype_ints(self, component_cls: type[NumericDateComponentBase], in_range_value: int, max_value: int) -> None:
        """Negated variant: argtype must not parse numeric strings."""
        assert self.validate("parses_argtype_ints", component_cls=component_cls, in_range_value=in_range_value, max_value=max_value)


class FailsArgtypeOnJunkMixinBase(Mixin, ABC):
    """Feature: argtype raises ValueError for unparseable CLI input."""

    fail_fails_argtype_on_junk: type[BaseException] = ValueError

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_argtype_on_junk":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            cls.argtype("definitely-not-a-value")
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsArgtypeOnJunkMixin(FailsArgtypeOnJunkMixinBase, ABC):
    negative_fails_argtype_on_junk: bool = False

    @pytest.mark.feature_argparse
    @pytest.mark.static
    def test_fails_argtype_on_junk(self, component_cls: type[NumericDateComponentBase]) -> None:
        """Positive variant (unused in practice; see NoFailsArgtypeOnJunkMixin)."""
        assert self.validate("fails_argtype_on_junk", component_cls=component_cls)


class NoFailsArgtypeOnJunkMixin(FailsArgtypeOnJunkMixinBase, ABC):
    negative_fails_argtype_on_junk: bool = True  # asserting variant for fail_* features

    @pytest.mark.feature_argparse
    @pytest.mark.static
    def test_fails_argtype_on_junk(self, component_cls: type[NumericDateComponentBase]) -> None:
        """argtype raises ValueError for non-numeric, non-name input."""
        assert self.validate("fails_argtype_on_junk", component_cls=component_cls)


# ------------------------------------------------------------------ arithmetic
class ShiftsWithinRangeMixinBase(Mixin, ABC):
    """Feature: + and - produce new, correctly shifted instances while the
    operands stay untouched. Only non-wrapping deltas are exercised here:
    wrap-around is defective (REPORT.md D2) and is excluded from this suite.
    Deltas must also keep results strictly below the max value, because D2
    corrupts even in-range results that land exactly on the upper bound."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NumericDateComponentBase]: ...

    @pytest.fixture
    @abstractmethod
    def in_range_value(self) -> int: ...

    @pytest.fixture
    @abstractmethod
    def safe_delta(self) -> int:
        """A delta that keeps in_range_value +/- delta inside the range."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "shifts_within_range":
            cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            value: int = kwargs["in_range_value"]
            delta: int = kwargs["safe_delta"]
            start = cls(value)
            forward = start + delta
            backward = start - delta
            return (
                forward.int_id == value + delta
                and backward.int_id == value - delta
                and start.int_id == value  # operands are immutable
                and type(forward) is cls
            )
        return super().condition(feature, *args, **kwargs)


class ShiftsWithinRangeMixin(ShiftsWithinRangeMixinBase, ABC):
    negative_shifts_within_range: bool = False

    @pytest.mark.feature_arithmetic
    def test_shifts_within_range(self, component_cls: type[NumericDateComponentBase], in_range_value: int, safe_delta: int) -> None:
        """Non-wrapping + / - return new shifted instances of the same type."""
        assert self.validate("shifts_within_range", component_cls=component_cls, in_range_value=in_range_value, safe_delta=safe_delta)


class NoShiftsWithinRangeMixin(ShiftsWithinRangeMixinBase, ABC):
    negative_shifts_within_range: bool = True

    @pytest.mark.feature_arithmetic
    def test_shifts_within_range(self, component_cls: type[NumericDateComponentBase], in_range_value: int, safe_delta: int) -> None:
        """Negated variant: shifting must not behave linearly."""
        assert self.validate("shifts_within_range", component_cls=component_cls, in_range_value=in_range_value, safe_delta=safe_delta)


# ------------------------------------------------------------- grouping mixins
class PlainNumericComponentMixins(
    ConstructsFromIntMixin,
    ClampsOutOfRangeIntsMixin,
    NormalizesIntsStaticallyMixin,
    NoFailsOnBoolConstructionMixin,
    RejectsStringValuesMixin,
    ComparesByIntIdMixin,
    CopiesViaCreateFromMixin,
    ParsesArgtypeIntsMixin,
    NoFailsArgtypeOnJunkMixin,
    ShiftsWithinRangeMixin,
    ABC,
):
    """Group: the full expected behavior of a plain numeric component."""
