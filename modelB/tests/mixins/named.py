"""
Feature mixins for named date components (Month, Weekday, Season, Hour).

IMPORTANT: the shipped classes cannot be instantiated on Python 3.12+ because
`get_args()` on a PEP 695 `type` alias returns `()` (see REPORT.md, defect D1
and tests/test_rejections.py). To still verify the *logic* of the shipped
methods through the documented extension contract ("Subclasses must define
_NAMES, _MIN, and _MAX"), each test file derives a subclass that provides the
intended _NAMES list and runs these features against it.
"""
from abc import ABC
from typing import Any

import pytest

from datecomponents.base import NamedNumericDateComponentBase
from tests.mixins.numeric import ComponentFixturesMixin


class NamedComponentFixturesMixin(ComponentFixturesMixin, ABC):
    """Fixtures shared by the named-component features."""

    @pytest.fixture
    def component_cls(self) -> type[NamedNumericDateComponentBase[str]]:
        """Narrowed: the named component class under test."""
        raise NotImplementedError

    @pytest.fixture
    def valid_name(self) -> str:
        """The canonical (lowercase) name corresponding to `valid_int`."""
        raise NotImplementedError


# --- feature: accepts_name_case_insensitively --------------------------------

class AcceptsNameCaseInsensitivelyMixinBase(NamedComponentFixturesMixin, ABC):
    """Construction from a name matches case-insensitively -> canonical ids."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "accepts_name_case_insensitively":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            valid_name: str = kwargs["valid_name"]
            subject = component_cls(valid_name.upper())
            return subject.int_id == valid_int and subject.str_id == valid_name
        return super().condition(feature, *args, **kwargs)


class AcceptsNameCaseInsensitivelyMixin(AcceptsNameCaseInsensitivelyMixinBase, ABC):
    negative_accepts_name_case_insensitively: bool = False

    @pytest.mark.construction
    def test_accepts_name_case_insensitively(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        valid_int: int,
        valid_name: str,
    ) -> None:
        """An upper-cased name resolves to the matching int and canonical name."""
        assert self.validate(
            "accepts_name_case_insensitively",
            component_cls=component_cls,
            valid_int=valid_int,
            valid_name=valid_name,
        )


class NoAcceptsNameCaseInsensitivelyMixin(AcceptsNameCaseInsensitivelyMixin, ABC):
    negative_accepts_name_case_insensitively: bool = True


# --- feature: fails_with_unknown_name ------------------------------------------

class FailsWithUnknownNameMixinBase(NamedComponentFixturesMixin, ABC):
    """Unknown names raise ValueError from the constructor."""

    fail_fails_with_unknown_name: type[BaseException] = ValueError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_with_unknown_name":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            component_cls("definitely-not-a-real-name")
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsWithUnknownNameMixin(FailsWithUnknownNameMixinBase, ABC):
    negative_fails_with_unknown_name: bool = False

    @pytest.mark.construction
    def test_fails_with_unknown_name(
        self, component_cls: type[NamedNumericDateComponentBase[str]]
    ) -> None:
        """A made-up name raises ValueError (asserted inside validate)."""
        self.validate("fails_with_unknown_name", component_cls=component_cls)


class NoFailsWithUnknownNameMixin(FailsWithUnknownNameMixin, ABC):
    negative_fails_with_unknown_name: bool = True


# --- feature: str_returns_canonical_name -----------------------------------------

class StrReturnsCanonicalNameMixinBase(NamedComponentFixturesMixin, ABC):
    """str(component) and .str_id give the canonical lowercase name."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "str_returns_canonical_name":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            valid_name: str = kwargs["valid_name"]
            subject = component_cls(valid_int)
            return str(subject) == valid_name and subject.str_id == valid_name
        return super().condition(feature, *args, **kwargs)


class StrReturnsCanonicalNameMixin(StrReturnsCanonicalNameMixinBase, ABC):
    negative_str_returns_canonical_name: bool = False

    @pytest.mark.identity
    def test_str_returns_canonical_name(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        valid_int: int,
        valid_name: str,
    ) -> None:
        """Int construction exposes the matching canonical name via str()."""
        assert self.validate(
            "str_returns_canonical_name",
            component_cls=component_cls,
            valid_int=valid_int,
            valid_name=valid_name,
        )


class NoStrReturnsCanonicalNameMixin(StrReturnsCanonicalNameMixin, ABC):
    negative_str_returns_canonical_name: bool = True


# --- feature: setters_stay_in_sync ------------------------------------------------

class SettersStayInSyncMixinBase(NamedComponentFixturesMixin, ABC):
    """Assigning int_id updates str_id and vice versa (one conceptual feature)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "setters_stay_in_sync":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            valid_name: str = kwargs["valid_name"]
            # Start from the minimum value, then move via each setter in turn.
            via_int = component_cls(component_cls._MIN)
            via_int.int_id = valid_int
            via_str = component_cls(component_cls._MIN)
            via_str.str_id = valid_name
            return (
                via_int.str_id == valid_name
                and via_str.int_id == valid_int
            )
        return super().condition(feature, *args, **kwargs)


class SettersStayInSyncMixin(SettersStayInSyncMixinBase, ABC):
    negative_setters_stay_in_sync: bool = False

    @pytest.mark.identity
    def test_setters_stay_in_sync(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        valid_int: int,
        valid_name: str,
    ) -> None:
        """int_id and str_id setters keep the two representations aligned."""
        assert self.validate(
            "setters_stay_in_sync",
            component_cls=component_cls,
            valid_int=valid_int,
            valid_name=valid_name,
        )


class NoSettersStayInSyncMixin(SettersStayInSyncMixin, ABC):
    negative_setters_stay_in_sync: bool = True


# --- feature: create_from_name (classmethod) ----------------------------------------

class CreateFromNameMixinBase(NamedComponentFixturesMixin, ABC):
    """create_from also accepts a name for named components."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "create_from_name":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            valid_name: str = kwargs["valid_name"]
            return component_cls.create_from(valid_name).int_id == valid_int
        return super().condition(feature, *args, **kwargs)


class CreateFromNameMixin(CreateFromNameMixinBase, ABC):
    negative_create_from_name: bool = False

    @pytest.mark.construction
    @pytest.mark.static
    def test_create_from_name(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        valid_int: int,
        valid_name: str,
    ) -> None:
        """Classmethod create_from(name) resolves names like the constructor."""
        assert self.validate(
            "create_from_name",
            component_cls=component_cls,
            valid_int=valid_int,
            valid_name=valid_name,
        )


class NoCreateFromNameMixin(CreateFromNameMixin, ABC):
    negative_create_from_name: bool = True


# --- feature: normalize_str_from_int (classmethod) ----------------------------------

class NormalizeStrFromIntMixinBase(NamedComponentFixturesMixin, ABC):
    """normalize_str maps ints (clamped) and names to canonical names."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "normalize_str_from_int":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            valid_name: str = kwargs["valid_name"]
            return (
                component_cls.normalize_str(valid_int) == valid_name
                and component_cls.normalize_str(valid_name.title()) == valid_name
            )
        return super().condition(feature, *args, **kwargs)


class NormalizeStrFromIntMixin(NormalizeStrFromIntMixinBase, ABC):
    negative_normalize_str_from_int: bool = False

    @pytest.mark.normalization
    @pytest.mark.static
    def test_normalize_str_from_int(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        valid_int: int,
        valid_name: str,
    ) -> None:
        """Classmethod normalize_str canonicalizes both ints and names."""
        assert self.validate(
            "normalize_str_from_int",
            component_cls=component_cls,
            valid_int=valid_int,
            valid_name=valid_name,
        )


class NoNormalizeStrFromIntMixin(NormalizeStrFromIntMixin, ABC):
    negative_normalize_str_from_int: bool = True


# --- feature: fails_normalize_str_with_bad_type (classmethod) ------------------------

class FailsNormalizeStrWithBadTypeMixinBase(NamedComponentFixturesMixin, ABC):
    """normalize_str rejects values that are neither int nor str."""

    fail_fails_normalize_str_with_bad_type: type[BaseException] = TypeError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_normalize_str_with_bad_type":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            component_cls.normalize_str(1.5)  # type: ignore[arg-type]
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsNormalizeStrWithBadTypeMixin(FailsNormalizeStrWithBadTypeMixinBase, ABC):
    negative_fails_normalize_str_with_bad_type: bool = False

    @pytest.mark.normalization
    @pytest.mark.static
    def test_fails_normalize_str_with_bad_type(
        self, component_cls: type[NamedNumericDateComponentBase[str]]
    ) -> None:
        """normalize_str(float) raises TypeError (asserted inside validate)."""
        self.validate("fails_normalize_str_with_bad_type", component_cls=component_cls)


class NoFailsNormalizeStrWithBadTypeMixin(FailsNormalizeStrWithBadTypeMixin, ABC):
    negative_fails_normalize_str_with_bad_type: bool = True


# --- feature: fails_normalize_str_with_unknown_name (classmethod) ----------------------

class FailsNormalizeStrWithUnknownNameMixinBase(NamedComponentFixturesMixin, ABC):
    """normalize_str rejects strings that are not known names."""

    fail_fails_normalize_str_with_unknown_name: type[BaseException] = ValueError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_normalize_str_with_unknown_name":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            component_cls.normalize_str("definitely-not-a-real-name")
            return True  # pragma: no cover - the line above must raise
        return super().condition(feature, *args, **kwargs)


class FailsNormalizeStrWithUnknownNameMixin(FailsNormalizeStrWithUnknownNameMixinBase, ABC):
    negative_fails_normalize_str_with_unknown_name: bool = False

    @pytest.mark.normalization
    @pytest.mark.static
    def test_fails_normalize_str_with_unknown_name(
        self, component_cls: type[NamedNumericDateComponentBase[str]]
    ) -> None:
        """normalize_str('bogus') raises ValueError (asserted inside validate)."""
        self.validate(
            "fails_normalize_str_with_unknown_name", component_cls=component_cls
        )


class NoFailsNormalizeStrWithUnknownNameMixin(FailsNormalizeStrWithUnknownNameMixin, ABC):
    negative_fails_normalize_str_with_unknown_name: bool = True


# --- feature: argtype_parses_name (classmethod) ---------------------------------------

class ArgtypeParsesNameMixinBase(NamedComponentFixturesMixin, ABC):
    """Named argtype falls back to name resolution for non-numeric strings."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "argtype_parses_name":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            valid_name: str = kwargs["valid_name"]
            return (
                component_cls.argtype(valid_name) == valid_name
                and component_cls.argtype(str(valid_int)) == valid_int
            )
        return super().condition(feature, *args, **kwargs)


class ArgtypeParsesNameMixin(ArgtypeParsesNameMixinBase, ABC):
    negative_argtype_parses_name: bool = False

    @pytest.mark.argparse_support
    @pytest.mark.static
    def test_argtype_parses_name(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        valid_int: int,
        valid_name: str,
    ) -> None:
        """argtype returns a canonical name for names, an int for numbers."""
        assert self.validate(
            "argtype_parses_name",
            component_cls=component_cls,
            valid_int=valid_int,
            valid_name=valid_name,
        )


class NoArgtypeParsesNameMixin(ArgtypeParsesNameMixin, ABC):
    negative_argtype_parses_name: bool = True


# --- feature: resolves_alias -------------------------------------------------------

class ResolvesAliasMixinBase(NamedComponentFixturesMixin, ABC):
    """Alias inputs map to their canonical name (e.g. 'fall' -> 'autumn')."""

    @pytest.fixture
    def alias_name(self) -> str:
        """A registered alias for `canonical_of_alias`."""
        raise NotImplementedError

    @pytest.fixture
    def canonical_of_alias(self) -> str:
        """The canonical name the alias resolves to."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "resolves_alias":
            component_cls: type[NamedNumericDateComponentBase[str]] = kwargs["component_cls"]
            alias_name: str = kwargs["alias_name"]
            canonical: str = kwargs["canonical_of_alias"]
            subject = component_cls(alias_name.upper())  # aliases are case-insensitive too
            return subject.str_id == canonical and subject == component_cls(canonical)
        return super().condition(feature, *args, **kwargs)


class ResolvesAliasMixin(ResolvesAliasMixinBase, ABC):
    negative_resolves_alias: bool = False

    @pytest.mark.normalization
    def test_resolves_alias(
        self,
        component_cls: type[NamedNumericDateComponentBase[str]],
        alias_name: str,
        canonical_of_alias: str,
    ) -> None:
        """Registered aliases construct the same value as the canonical name."""
        assert self.validate(
            "resolves_alias",
            component_cls=component_cls,
            alias_name=alias_name,
            canonical_of_alias=canonical_of_alias,
        )


class NoResolvesAliasMixin(ResolvesAliasMixin, ABC):
    negative_resolves_alias: bool = True


# --- convenience group: everything shared by named components -------------------------

class NamedComponentMixin(
    AcceptsNameCaseInsensitivelyMixin,
    FailsWithUnknownNameMixin,
    StrReturnsCanonicalNameMixin,
    SettersStayInSyncMixin,
    CreateFromNameMixin,
    NormalizeStrFromIntMixin,
    FailsNormalizeStrWithBadTypeMixin,
    FailsNormalizeStrWithUnknownNameMixin,
    ArgtypeParsesNameMixin,
    ABC,
):
    """Empty grouping of every feature common to all named components."""
