"""
Feature mixins for `NamedNumericDateComponentBase` behavior and for the
optional-year behavior shared by Month and Season.
"""
import pytest
from abc import ABC, abstractmethod
from typing import Any

from test_utils import Mixin
from dateutils.base import NamedNumericDateComponentBase


# ---------------------------------------------------------------------- naming
class ConstructsFromNameMixinBase(Mixin, ABC):
    """Feature: a component can be built from a canonical name, case-insensitively."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]: ...

    @pytest.fixture
    @abstractmethod
    def sample_name(self) -> str:
        """A canonical (lowercase) name."""

    @pytest.fixture
    @abstractmethod
    def sample_name_int(self) -> int:
        """The int the sample name maps to."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "constructs_from_name":
            cls: type[NamedNumericDateComponentBase[Any]] = kwargs["component_cls"]
            name: str = kwargs["sample_name"]
            expected: int = kwargs["sample_name_int"]
            obj = cls(name)
            shouty = cls(name.upper())  # case-insensitive matching
            return (
                obj.int_id == expected
                and obj.str_id == name
                and shouty.str_id == name
                and str(obj) == name  # __str__ mirrors str_id
            )
        return super().condition(feature, *args, **kwargs)


class ConstructsFromNameMixin(ConstructsFromNameMixinBase, ABC):
    negative_constructs_from_name: bool = False

    @pytest.mark.feature_naming
    def test_constructs_from_name(self, component_cls: type[NamedNumericDateComponentBase[Any]], sample_name: str, sample_name_int: int) -> None:
        """Names construct components case-insensitively; str() is canonical."""
        assert self.validate("constructs_from_name", component_cls=component_cls, sample_name=sample_name, sample_name_int=sample_name_int)


class NoConstructsFromNameMixin(ConstructsFromNameMixinBase, ABC):
    negative_constructs_from_name: bool = True

    @pytest.mark.feature_naming
    def test_constructs_from_name(self, component_cls: type[NamedNumericDateComponentBase[Any]], sample_name: str, sample_name_int: int) -> None:
        """Negated variant: name construction must not work."""
        assert self.validate("constructs_from_name", component_cls=component_cls, sample_name=sample_name, sample_name_int=sample_name_int)


class FailsOnInvalidNameMixinBase(Mixin, ABC):
    """Feature: unknown names raise ValueError at construction."""

    fail_fails_on_invalid_name: type[BaseException] = ValueError

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_on_invalid_name":
            cls: type[NamedNumericDateComponentBase[Any]] = kwargs["component_cls"]
            cls("smarch")  # famously not a real date component
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsOnInvalidNameMixin(FailsOnInvalidNameMixinBase, ABC):
    negative_fails_on_invalid_name: bool = False

    @pytest.mark.feature_naming
    def test_fails_on_invalid_name(self, component_cls: type[NamedNumericDateComponentBase[Any]]) -> None:
        """Positive variant (unused in practice; see NoFailsOnInvalidNameMixin)."""
        assert self.validate("fails_on_invalid_name", component_cls=component_cls)


class NoFailsOnInvalidNameMixin(FailsOnInvalidNameMixinBase, ABC):
    negative_fails_on_invalid_name: bool = True  # asserting variant for fail_* features

    @pytest.mark.feature_naming
    def test_fails_on_invalid_name(self, component_cls: type[NamedNumericDateComponentBase[Any]]) -> None:
        """Unknown names raise ValueError."""
        assert self.validate("fails_on_invalid_name", component_cls=component_cls)


class SyncsStrAndIntIdsMixinBase(Mixin, ABC):
    """Feature: the two id properties stay in sync through either setter."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]: ...

    @pytest.fixture
    @abstractmethod
    def sample_name(self) -> str: ...

    @pytest.fixture
    @abstractmethod
    def sample_name_int(self) -> int: ...

    @pytest.fixture
    @abstractmethod
    def other_name(self) -> str:
        """A second canonical name, different from sample_name."""

    @pytest.fixture
    @abstractmethod
    def other_name_int(self) -> int: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "syncs_str_and_int_ids":
            cls: type[NamedNumericDateComponentBase[Any]] = kwargs["component_cls"]
            obj = cls(kwargs["sample_name"])
            obj.int_id = kwargs["other_name_int"]  # int setter refreshes str_id
            synced_from_int = obj.str_id == kwargs["other_name"]
            obj.str_id = kwargs["sample_name"]  # str setter refreshes int_id
            synced_from_str = obj.int_id == kwargs["sample_name_int"]
            return synced_from_int and synced_from_str
        return super().condition(feature, *args, **kwargs)


class SyncsStrAndIntIdsMixin(SyncsStrAndIntIdsMixinBase, ABC):
    negative_syncs_str_and_int_ids: bool = False

    @pytest.mark.feature_naming
    def test_syncs_str_and_int_ids(self, component_cls: type[NamedNumericDateComponentBase[Any]], sample_name: str, sample_name_int: int, other_name: str, other_name_int: int) -> None:
        """Setting either id updates the other representation."""
        assert self.validate("syncs_str_and_int_ids", component_cls=component_cls, sample_name=sample_name, sample_name_int=sample_name_int, other_name=other_name, other_name_int=other_name_int)


class NoSyncsStrAndIntIdsMixin(SyncsStrAndIntIdsMixinBase, ABC):
    negative_syncs_str_and_int_ids: bool = True

    @pytest.mark.feature_naming
    def test_syncs_str_and_int_ids(self, component_cls: type[NamedNumericDateComponentBase[Any]], sample_name: str, sample_name_int: int, other_name: str, other_name_int: int) -> None:
        """Negated variant: the ids must not stay in sync."""
        assert self.validate("syncs_str_and_int_ids", component_cls=component_cls, sample_name=sample_name, sample_name_int=sample_name_int, other_name=other_name, other_name_int=other_name_int)


class NormalizesNamesStaticallyMixinBase(Mixin, ABC):
    """Feature: class-level helpers handle names without an instance
    (static test): create_from(name), argtype(name) and normalize_str(int)."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]: ...

    @pytest.fixture
    @abstractmethod
    def sample_name(self) -> str: ...

    @pytest.fixture
    @abstractmethod
    def sample_name_int(self) -> int: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "normalizes_names_statically":
            cls: type[NamedNumericDateComponentBase[Any]] = kwargs["component_cls"]
            name: str = kwargs["sample_name"]
            expected: int = kwargs["sample_name_int"]
            return (
                cls.create_from(name).int_id == expected
                and cls.argtype(name.upper()) == name  # falls back to name parsing
                and cls.argtype(str(expected)) == expected  # int fast-path
                and cls.normalize_str(expected) == name
                and cls.normalize_int(name) == expected
            )
        return super().condition(feature, *args, **kwargs)


class NormalizesNamesStaticallyMixin(NormalizesNamesStaticallyMixinBase, ABC):
    negative_normalizes_names_statically: bool = False

    @pytest.mark.feature_naming
    @pytest.mark.feature_argparse
    @pytest.mark.static
    def test_normalizes_names_statically(self, component_cls: type[NamedNumericDateComponentBase[Any]], sample_name: str, sample_name_int: int) -> None:
        """create_from/argtype/normalize_* accept names at class level."""
        assert self.validate("normalizes_names_statically", component_cls=component_cls, sample_name=sample_name, sample_name_int=sample_name_int)


class NoNormalizesNamesStaticallyMixin(NormalizesNamesStaticallyMixinBase, ABC):
    negative_normalizes_names_statically: bool = True

    @pytest.mark.feature_naming
    @pytest.mark.feature_argparse
    @pytest.mark.static
    def test_normalizes_names_statically(self, component_cls: type[NamedNumericDateComponentBase[Any]], sample_name: str, sample_name_int: int) -> None:
        """Negated variant: class-level name handling must not work."""
        assert self.validate("normalizes_names_statically", component_cls=component_cls, sample_name=sample_name, sample_name_int=sample_name_int)


class FailsNormalizeStrOnNonStringMixinBase(Mixin, ABC):
    """Feature: normalize_str rejects values that are neither int nor str."""

    fail_fails_normalize_str_on_non_string: type[BaseException] = TypeError

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "fails_normalize_str_on_non_string":
            cls: type[NamedNumericDateComponentBase[Any]] = kwargs["component_cls"]
            cls.normalize_str(1.5)  # type: ignore[arg-type]  # deliberate misuse
            return True  # pragma: no cover - unreachable when the guard works
        return super().condition(feature, *args, **kwargs)


class FailsNormalizeStrOnNonStringMixin(FailsNormalizeStrOnNonStringMixinBase, ABC):
    negative_fails_normalize_str_on_non_string: bool = False

    @pytest.mark.feature_naming
    @pytest.mark.static
    def test_fails_normalize_str_on_non_string(self, component_cls: type[NamedNumericDateComponentBase[Any]]) -> None:
        """Positive variant (unused in practice)."""
        assert self.validate("fails_normalize_str_on_non_string", component_cls=component_cls)


class NoFailsNormalizeStrOnNonStringMixin(FailsNormalizeStrOnNonStringMixinBase, ABC):
    negative_fails_normalize_str_on_non_string: bool = True  # asserting variant

    @pytest.mark.feature_naming
    @pytest.mark.static
    def test_fails_normalize_str_on_non_string(self, component_cls: type[NamedNumericDateComponentBase[Any]]) -> None:
        """normalize_str raises TypeError for non-int/non-str values."""
        assert self.validate("fails_normalize_str_on_non_string", component_cls=component_cls)


# --------------------------------------------------------------------- aliases
class ResolvesAliasesMixinBase(Mixin, ABC):
    """Feature: alias names resolve to their canonical equivalents."""

    @pytest.fixture
    @abstractmethod
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]: ...

    @pytest.fixture
    @abstractmethod
    def alias_name(self) -> str:
        """A registered alias."""

    @pytest.fixture
    @abstractmethod
    def canonical_name(self) -> str:
        """The canonical name the alias resolves to."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "resolves_aliases":
            cls: type[NamedNumericDateComponentBase[Any]] = kwargs["component_cls"]
            alias: str = kwargs["alias_name"]
            canonical: str = kwargs["canonical_name"]
            obj = cls(alias)
            return (
                obj.str_id == canonical  # aliases never become the stored id
                and obj == cls(canonical)
                and cls.normalize_str(alias.upper()) == canonical
            )
        return super().condition(feature, *args, **kwargs)


class ResolvesAliasesMixin(ResolvesAliasesMixinBase, ABC):
    negative_resolves_aliases: bool = False

    @pytest.mark.feature_aliases
    def test_resolves_aliases(self, component_cls: type[NamedNumericDateComponentBase[Any]], alias_name: str, canonical_name: str) -> None:
        """Alias names construct/normalize to their canonical form."""
        assert self.validate("resolves_aliases", component_cls=component_cls, alias_name=alias_name, canonical_name=canonical_name)


class NoResolvesAliasesMixin(ResolvesAliasesMixinBase, ABC):
    negative_resolves_aliases: bool = True

    @pytest.mark.feature_aliases
    def test_resolves_aliases(self, component_cls: type[NamedNumericDateComponentBase[Any]], alias_name: str, canonical_name: str) -> None:
        """Negated variant: aliases must not resolve."""
        assert self.validate("resolves_aliases", component_cls=component_cls, alias_name=alias_name, canonical_name=canonical_name)


# --------------------------------------------------------------- year tracking
class TracksOptionalYearMixinBase(Mixin, ABC):
    """Feature: Month/Season optionally carry a year; 1970 is the default."""

    @pytest.fixture
    @abstractmethod
    def yeared_cls(self) -> type[Any]:
        """A component class whose __init__ accepts (value, year)."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "tracks_optional_year":
            cls: type[Any] = kwargs["yeared_cls"]
            with_year = cls(1, 2024)
            without_year = cls(1)
            return (
                with_year.has_year()
                and with_year.year_or_default() == 2024
                and not without_year.has_year()
                and without_year.year_or_default() == 1970
            )
        return super().condition(feature, *args, **kwargs)


class TracksOptionalYearMixin(TracksOptionalYearMixinBase, ABC):
    negative_tracks_optional_year: bool = False

    @pytest.mark.feature_year_tracking
    def test_tracks_optional_year(self, yeared_cls: type[Any]) -> None:
        """has_year/year_or_default reflect the optional year (default 1970)."""
        assert self.validate("tracks_optional_year", yeared_cls=yeared_cls)


class NoTracksOptionalYearMixin(TracksOptionalYearMixinBase, ABC):
    negative_tracks_optional_year: bool = True

    @pytest.mark.feature_year_tracking
    def test_tracks_optional_year(self, yeared_cls: type[Any]) -> None:
        """Negated variant: the year must not be tracked."""
        assert self.validate("tracks_optional_year", yeared_cls=yeared_cls)


class YearAwareEqualityMixinBase(Mixin, ABC):
    """Feature: equality/hash include the year, unlike the plain int_id
    comparison of the base class. This feature therefore overrides (negates)
    `compares_by_int_id` when both are combined on one test class."""

    @pytest.fixture
    @abstractmethod
    def yeared_cls(self) -> type[Any]: ...

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "year_aware_equality":
            cls: type[Any] = kwargs["yeared_cls"]
            return (
                cls(1, 2024) == cls(1, 2024)
                and cls(1, 2024) != cls(1, 2025)  # same value, different year
                and cls(1, 2024) != cls(2, 2024)  # different value, same year
                and cls(1, 2024) != "1"  # foreign types compare unequal
                and hash(cls(1, 2024)) == hash(cls(1, 2024))
                and hash(cls(1, 2024)) != hash(cls(1, 2025))
            )
        return super().condition(feature, *args, **kwargs)


class YearAwareEqualityMixin(YearAwareEqualityMixinBase, ABC):
    negative_year_aware_equality: bool = False

    @pytest.mark.feature_equality
    @pytest.mark.feature_year_tracking
    def test_year_aware_equality(self, yeared_cls: type[Any]) -> None:
        """Equality and hashing take the optional year into account."""
        assert self.validate("year_aware_equality", yeared_cls=yeared_cls)


class NoYearAwareEqualityMixin(YearAwareEqualityMixinBase, ABC):
    negative_year_aware_equality: bool = True

    @pytest.mark.feature_equality
    @pytest.mark.feature_year_tracking
    def test_year_aware_equality(self, yeared_cls: type[Any]) -> None:
        """Negated variant: equality must ignore the year."""
        assert self.validate("year_aware_equality", yeared_cls=yeared_cls)


# ------------------------------------------------------------- grouping mixins
class NamedComponentMixins(
    ConstructsFromNameMixin,
    NoFailsOnInvalidNameMixin,
    SyncsStrAndIntIdsMixin,
    NormalizesNamesStaticallyMixin,
    NoFailsNormalizeStrOnNonStringMixin,
    ABC,
):
    """Group: the naming behavior every named component must provide."""


class YearedComponentMixins(TracksOptionalYearMixin, YearAwareEqualityMixin, ABC):
    """Group: the optional-year behavior shared by Month and Season."""
