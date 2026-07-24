"""
Feature mixins shared by every numeric date component (Minute, Second, and the
named components, which inherit all of this behavior from the same base class).

Each feature follows the standard Bedrock layout:

* ``<Feature>MixinBase`` - abstract; implements ``condition`` for exactly one
  feature (the snake_case of the class name minus ``MixinBase``) and declares,
  but does not implement, the fixtures the condition needs.
* ``<Feature>Mixin``     - abstract; ``negative_<feature> = False`` and the
  ``test_...`` methods, which only call ``self.validate``.
* ``No<Feature>Mixin``   - abstract; extends the positive mixin so it inherits
  its tests, flipping ``negative_<feature>`` to True.

Bases whose names begin with ``Fails`` set a non-False ``fail_<feature>``;
``validate`` then asserts the expected exception via ``pytest.raises``, so
their tests are bare ``self.validate`` calls (the return value carries no
meaning once the exception is the assertion).

None of these classes start with ``Test``, so pytest never collects them
directly; only the concrete test classes in the ``test_*.py`` files are run.
"""
from abc import ABC
from typing import Any

import pytest

from datecomponents.base import NumericDateComponentBase
from tests.test_utils import Mixin


class ComponentFixturesMixin(Mixin, ABC):
    """Declares the fixtures every numeric-component feature relies on."""

    @pytest.fixture
    def component_cls(self) -> type[NumericDateComponentBase]:
        """The component class under test. Implemented by each test class."""
        raise NotImplementedError

    @pytest.fixture
    def valid_int(self) -> int:
        """An in-range integer value, strictly between _MIN and _MAX."""
        raise NotImplementedError


# --- feature: accepts_in_range_int -----------------------------------------

class AcceptsInRangeIntMixinBase(ComponentFixturesMixin, ABC):
    """Constructing from an in-range int stores that exact value."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "accepts_in_range_int":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return component_cls(valid_int).int_id == valid_int
        return super().condition(feature, *args, **kwargs)


class AcceptsInRangeIntMixin(AcceptsInRangeIntMixinBase, ABC):
    negative_accepts_in_range_int: bool = False

    @pytest.mark.construction
    def test_accepts_in_range_int(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """An in-range integer passed to the constructor is kept verbatim."""
        assert self.validate(
            "accepts_in_range_int", component_cls=component_cls, valid_int=valid_int
        )


class NoAcceptsInRangeIntMixin(AcceptsInRangeIntMixin, ABC):
    negative_accepts_in_range_int: bool = True


# --- feature: clamps_out_of_range_int ---------------------------------------

class ClampsOutOfRangeIntMixinBase(ComponentFixturesMixin, ABC):
    """Out-of-range ints are silently clamped to _MIN/_MAX (documented)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "clamps_out_of_range_int":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            # Values far outside the range land exactly on the bounds.
            below = component_cls(component_cls._MIN - 100)
            above = component_cls(component_cls._MAX + 100)
            return (
                below.int_id == component_cls._MIN
                and above.int_id == component_cls._MAX
            )
        return super().condition(feature, *args, **kwargs)


class ClampsOutOfRangeIntMixin(ClampsOutOfRangeIntMixinBase, ABC):
    negative_clamps_out_of_range_int: bool = False

    @pytest.mark.normalization
    def test_clamps_out_of_range_int(
        self, component_cls: type[NumericDateComponentBase]
    ) -> None:
        """Constructor clamps ints below _MIN up and above _MAX down."""
        assert self.validate("clamps_out_of_range_int", component_cls=component_cls)


class NoClampsOutOfRangeIntMixin(ClampsOutOfRangeIntMixin, ABC):
    negative_clamps_out_of_range_int: bool = True


# --- feature: fails_with_non_int_type (constructor rejects bool/float) ------

class FailsWithNonIntTypeMixinBase(ComponentFixturesMixin, ABC):
    """The constructor rejects non-int types (bools included) with TypeError."""

    fail_fails_with_non_int_type: type[BaseException] = TypeError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_with_non_int_type":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            # bool is deliberately excluded by the `type() is int` check.
            component_cls(True)  # type: ignore[arg-type]
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsWithNonIntTypeMixin(FailsWithNonIntTypeMixinBase, ABC):
    negative_fails_with_non_int_type: bool = False

    @pytest.mark.construction
    def test_fails_with_non_int_type(
        self, component_cls: type[NumericDateComponentBase]
    ) -> None:
        """Passing a bool raises TypeError (asserted inside validate)."""
        self.validate("fails_with_non_int_type", component_cls=component_cls)


class NoFailsWithNonIntTypeMixin(FailsWithNonIntTypeMixin, ABC):
    negative_fails_with_non_int_type: bool = True


# --- feature: int_id_setter_renormalizes ------------------------------------

class IntIdSetterRenormalizesMixinBase(ComponentFixturesMixin, ABC):
    """Assigning int_id re-runs normalization (clamping) on the new value."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "int_id_setter_renormalizes":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            subject = component_cls(valid_int)
            subject.int_id = component_cls._MAX + 100
            return subject.int_id == component_cls._MAX
        return super().condition(feature, *args, **kwargs)


class IntIdSetterRenormalizesMixin(IntIdSetterRenormalizesMixinBase, ABC):
    negative_int_id_setter_renormalizes: bool = False

    @pytest.mark.normalization
    def test_int_id_setter_renormalizes(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """Setting .int_id after construction clamps just like the constructor."""
        assert self.validate(
            "int_id_setter_renormalizes",
            component_cls=component_cls,
            valid_int=valid_int,
        )


class NoIntIdSetterRenormalizesMixin(IntIdSetterRenormalizesMixin, ABC):
    negative_int_id_setter_renormalizes: bool = True


# --- feature: equal_when_same_value ------------------------------------------

class EqualWhenSameValueMixinBase(ComponentFixturesMixin, ABC):
    """Two instances of the same class and value compare equal."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "equal_when_same_value":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return component_cls(valid_int) == component_cls(valid_int)
        return super().condition(feature, *args, **kwargs)


class EqualWhenSameValueMixin(EqualWhenSameValueMixinBase, ABC):
    negative_equal_when_same_value: bool = False

    @pytest.mark.identity
    def test_equal_when_same_value(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """Value equality holds between independently built instances."""
        assert self.validate(
            "equal_when_same_value", component_cls=component_cls, valid_int=valid_int
        )


class NoEqualWhenSameValueMixin(EqualWhenSameValueMixin, ABC):
    negative_equal_when_same_value: bool = True


# --- feature: equal_to_other_type --------------------------------------------

class EqualToOtherTypeMixinBase(ComponentFixturesMixin, ABC):
    """
    Comparison against an unrelated object. __eq__ returns NotImplemented for
    foreign types, so `==` falls back to identity and yields False; the test
    classes therefore always mix in the *No* variant of this feature.
    """

    @pytest.fixture
    def other_typed_value(self) -> object:
        """A value of a different type holding the same underlying int."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "equal_to_other_type":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return component_cls(valid_int) == kwargs["other_typed_value"]
        return super().condition(feature, *args, **kwargs)


class EqualToOtherTypeMixin(EqualToOtherTypeMixinBase, ABC):
    negative_equal_to_other_type: bool = False

    @pytest.mark.identity
    def test_equal_to_other_type(
        self,
        component_cls: type[NumericDateComponentBase],
        valid_int: int,
        other_typed_value: object,
    ) -> None:
        """Cross-type equality must not hold, even for the same numeric value."""
        assert self.validate(
            "equal_to_other_type",
            component_cls=component_cls,
            valid_int=valid_int,
            other_typed_value=other_typed_value,
        )


class NoEqualToOtherTypeMixin(EqualToOtherTypeMixin, ABC):
    negative_equal_to_other_type: bool = True


# --- feature: hash_matches_equal_instance ------------------------------------

class HashMatchesEqualInstanceMixinBase(ComponentFixturesMixin, ABC):
    """Equal instances hash identically (dict/set safety)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "hash_matches_equal_instance":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return hash(component_cls(valid_int)) == hash(component_cls(valid_int))
        return super().condition(feature, *args, **kwargs)


class HashMatchesEqualInstanceMixin(HashMatchesEqualInstanceMixinBase, ABC):
    negative_hash_matches_equal_instance: bool = False

    @pytest.mark.identity
    def test_hash_matches_equal_instance(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """hash() agrees for equal instances, as required by the hash contract."""
        assert self.validate(
            "hash_matches_equal_instance",
            component_cls=component_cls,
            valid_int=valid_int,
        )


class NoHashMatchesEqualInstanceMixin(HashMatchesEqualInstanceMixin, ABC):
    negative_hash_matches_equal_instance: bool = True


# --- feature: converts_to_int -------------------------------------------------

class ConvertsToIntMixinBase(ComponentFixturesMixin, ABC):
    """int(component) returns the stored integer id."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "converts_to_int":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return int(component_cls(valid_int)) == valid_int
        return super().condition(feature, *args, **kwargs)


class ConvertsToIntMixin(ConvertsToIntMixinBase, ABC):
    negative_converts_to_int: bool = False

    @pytest.mark.identity
    def test_converts_to_int(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """int() round-trips the constructor argument."""
        assert self.validate(
            "converts_to_int", component_cls=component_cls, valid_int=valid_int
        )


class NoConvertsToIntMixin(ConvertsToIntMixin, ABC):
    negative_converts_to_int: bool = True


# --- feature: adds_within_range ------------------------------------------------

class AddsWithinRangeMixinBase(ComponentFixturesMixin, ABC):
    """
    `component + delta` produces a new instance with the summed value, as long
    as the result stays strictly inside the range (wrap-around behavior is
    defective - see the rejections file - so it is not asserted here).
    """

    @pytest.fixture
    def add_delta(self) -> int:
        """A delta keeping valid_int + delta strictly below _MAX."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "adds_within_range":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            add_delta: int = kwargs["add_delta"]
            subject = component_cls(valid_int)
            result = subject + add_delta
            # A new object is returned and the original is untouched.
            return (
                result is not subject
                and result.int_id == valid_int + add_delta
                and subject.int_id == valid_int
            )
        return super().condition(feature, *args, **kwargs)


class AddsWithinRangeMixin(AddsWithinRangeMixinBase, ABC):
    negative_adds_within_range: bool = False

    @pytest.mark.arithmetic
    def test_adds_within_range(
        self,
        component_cls: type[NumericDateComponentBase],
        valid_int: int,
        add_delta: int,
    ) -> None:
        """Non-wrapping addition returns a new, correctly valued instance."""
        assert self.validate(
            "adds_within_range",
            component_cls=component_cls,
            valid_int=valid_int,
            add_delta=add_delta,
        )


class NoAddsWithinRangeMixin(AddsWithinRangeMixin, ABC):
    negative_adds_within_range: bool = True


# --- feature: subtracts_within_range -------------------------------------------

class SubtractsWithinRangeMixinBase(ComponentFixturesMixin, ABC):
    """`component - delta` mirrors addition for results above _MIN."""

    @pytest.fixture
    def sub_delta(self) -> int:
        """A delta keeping valid_int - delta at or above _MIN (landing
        exactly on _MIN is safe; only crossing below it would wrap)."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "subtracts_within_range":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            sub_delta: int = kwargs["sub_delta"]
            return (component_cls(valid_int) - sub_delta).int_id == valid_int - sub_delta
        return super().condition(feature, *args, **kwargs)


class SubtractsWithinRangeMixin(SubtractsWithinRangeMixinBase, ABC):
    negative_subtracts_within_range: bool = False

    @pytest.mark.arithmetic
    def test_subtracts_within_range(
        self,
        component_cls: type[NumericDateComponentBase],
        valid_int: int,
        sub_delta: int,
    ) -> None:
        """Non-wrapping subtraction returns the decremented value."""
        assert self.validate(
            "subtracts_within_range",
            component_cls=component_cls,
            valid_int=valid_int,
            sub_delta=sub_delta,
        )


class NoSubtractsWithinRangeMixin(SubtractsWithinRangeMixin, ABC):
    negative_subtracts_within_range: bool = True


# --- feature: create_from_int (classmethod) -------------------------------------

class CreateFromIntMixinBase(ComponentFixturesMixin, ABC):
    """create_from accepts a plain int and builds an instance from it."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "create_from_int":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return component_cls.create_from(valid_int) == component_cls(valid_int)
        return super().condition(feature, *args, **kwargs)


class CreateFromIntMixin(CreateFromIntMixinBase, ABC):
    negative_create_from_int: bool = False

    @pytest.mark.construction
    @pytest.mark.static
    def test_create_from_int(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """Classmethod create_from(int) equals direct construction."""
        assert self.validate(
            "create_from_int", component_cls=component_cls, valid_int=valid_int
        )


class NoCreateFromIntMixin(CreateFromIntMixin, ABC):
    negative_create_from_int: bool = True


# --- feature: create_from_instance_copies (classmethod) --------------------------

class CreateFromInstanceCopiesMixinBase(ComponentFixturesMixin, ABC):
    """create_from(instance) returns an equal but distinct copy."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "create_from_instance_copies":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            original = component_cls(valid_int)
            copy = component_cls.create_from(original)
            return copy == original and copy is not original
        return super().condition(feature, *args, **kwargs)


class CreateFromInstanceCopiesMixin(CreateFromInstanceCopiesMixinBase, ABC):
    negative_create_from_instance_copies: bool = False

    @pytest.mark.construction
    @pytest.mark.static
    def test_create_from_instance_copies(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """create_from(instance) produces an equal copy, not the same object."""
        assert self.validate(
            "create_from_instance_copies",
            component_cls=component_cls,
            valid_int=valid_int,
        )


class NoCreateFromInstanceCopiesMixin(CreateFromInstanceCopiesMixin, ABC):
    negative_create_from_instance_copies: bool = True


# --- feature: normalize_int_clamps (classmethod) ----------------------------------

class NormalizeIntClampsMixinBase(ComponentFixturesMixin, ABC):
    """normalize_int clamps without needing an instance."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "normalize_int_clamps":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return (
                component_cls.normalize_int(valid_int) == valid_int
                and component_cls.normalize_int(component_cls._MAX + 1)
                == component_cls._MAX
            )
        return super().condition(feature, *args, **kwargs)


class NormalizeIntClampsMixin(NormalizeIntClampsMixinBase, ABC):
    negative_normalize_int_clamps: bool = False

    @pytest.mark.normalization
    @pytest.mark.static
    def test_normalize_int_clamps(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """Classmethod normalize_int passes valid values and clamps excess."""
        assert self.validate(
            "normalize_int_clamps", component_cls=component_cls, valid_int=valid_int
        )


class NoNormalizeIntClampsMixin(NormalizeIntClampsMixin, ABC):
    negative_normalize_int_clamps: bool = True


# --- feature: argtype_parses_numeric_string (classmethod) --------------------------

class ArgtypeParsesNumericStringMixinBase(ComponentFixturesMixin, ABC):
    """argtype converts a numeric string into a normalized int."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "argtype_parses_numeric_string":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            return component_cls.argtype(str(valid_int)) == valid_int
        return super().condition(feature, *args, **kwargs)


class ArgtypeParsesNumericStringMixin(ArgtypeParsesNumericStringMixinBase, ABC):
    negative_argtype_parses_numeric_string: bool = False

    @pytest.mark.argparse_support
    @pytest.mark.static
    def test_argtype_parses_numeric_string(
        self, component_cls: type[NumericDateComponentBase], valid_int: int
    ) -> None:
        """argtype('5') -> 5, ready for argparse `type=` usage."""
        assert self.validate(
            "argtype_parses_numeric_string",
            component_cls=component_cls,
            valid_int=valid_int,
        )


class NoArgtypeParsesNumericStringMixin(ArgtypeParsesNumericStringMixin, ABC):
    negative_argtype_parses_numeric_string: bool = True


# --- feature: fails_argtype_with_non_numeric (classmethod, numeric-only) ------------

class FailsArgtypeWithNonNumericMixinBase(ComponentFixturesMixin, ABC):
    """Plain numeric components reject non-numeric argtype input (ValueError)."""

    fail_fails_argtype_with_non_numeric: type[BaseException] = ValueError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_argtype_with_non_numeric":
            component_cls: type[NumericDateComponentBase] = kwargs["component_cls"]
            component_cls.argtype("not-a-number")
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsArgtypeWithNonNumericMixin(FailsArgtypeWithNonNumericMixinBase, ABC):
    negative_fails_argtype_with_non_numeric: bool = False

    @pytest.mark.argparse_support
    @pytest.mark.static
    def test_fails_argtype_with_non_numeric(
        self, component_cls: type[NumericDateComponentBase]
    ) -> None:
        """argtype raises ValueError for text on name-less components."""
        self.validate("fails_argtype_with_non_numeric", component_cls=component_cls)


class NoFailsArgtypeWithNonNumericMixin(FailsArgtypeWithNonNumericMixin, ABC):
    negative_fails_argtype_with_non_numeric: bool = True


# --- convenience group: everything shared by plain numeric components ---------------

class PlainNumericComponentMixin(
    AcceptsInRangeIntMixin,
    ClampsOutOfRangeIntMixin,
    FailsWithNonIntTypeMixin,
    IntIdSetterRenormalizesMixin,
    EqualWhenSameValueMixin,
    NoEqualToOtherTypeMixin,
    HashMatchesEqualInstanceMixin,
    ConvertsToIntMixin,
    AddsWithinRangeMixin,
    SubtractsWithinRangeMixin,
    CreateFromIntMixin,
    CreateFromInstanceCopiesMixin,
    NormalizeIntClampsMixin,
    ArgtypeParsesNumericStringMixin,
    ABC,
):
    """Empty grouping of every feature a bare numeric component supports."""
