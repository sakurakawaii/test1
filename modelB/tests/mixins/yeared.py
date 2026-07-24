"""
Feature mixins for year-carrying components (Month and Season).

These cover the optional `year` attribute: presence checks, the 1970
fallback, and year-sensitive equality/hashing.
"""
from abc import ABC
from typing import Any, Protocol

import pytest

from tests.test_utils import Mixin


class YearedComponent(Protocol):
    """Structural type for the shared Month/Season year API."""

    year: int | None

    def has_year(self) -> bool: ...
    def year_or_default(self) -> int: ...


class YearedFixturesMixin(Mixin, ABC):
    """Fixtures shared by the year-related features."""

    @pytest.fixture
    def yeared_subject(self) -> YearedComponent:
        """The component instance under test (with or without a year)."""
        raise NotImplementedError

    @pytest.fixture
    def expected_year(self) -> int:
        """The year the positive test classes construct their subject with."""
        raise NotImplementedError


# --- feature: has_year ---------------------------------------------------------

class HasYearMixinBase(YearedFixturesMixin, ABC):
    """has_year() reports whether a year was supplied."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "has_year":
            subject: YearedComponent = kwargs["yeared_subject"]
            return subject.has_year()
        return super().condition(feature, *args, **kwargs)


class HasYearMixin(HasYearMixinBase, ABC):
    negative_has_year: bool = False

    @pytest.mark.calendar
    def test_has_year(self, yeared_subject: YearedComponent) -> None:
        """has_year() is True when a year was given (negated by year-less subclasses)."""
        assert self.validate("has_year", yeared_subject=yeared_subject)


class NoHasYearMixin(HasYearMixin, ABC):
    negative_has_year: bool = True


# --- feature: year_or_default_returns_own_year -----------------------------------

class YearOrDefaultReturnsOwnYearMixinBase(YearedFixturesMixin, ABC):
    """year_or_default() returns the stored year when one is present."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "year_or_default_returns_own_year":
            subject: YearedComponent = kwargs["yeared_subject"]
            expected_year: int = kwargs["expected_year"]
            return subject.year_or_default() == expected_year
        return super().condition(feature, *args, **kwargs)


class YearOrDefaultReturnsOwnYearMixin(YearOrDefaultReturnsOwnYearMixinBase, ABC):
    negative_year_or_default_returns_own_year: bool = False

    @pytest.mark.calendar
    def test_year_or_default_returns_own_year(
        self, yeared_subject: YearedComponent, expected_year: int
    ) -> None:
        """year_or_default() echoes the construction year when set."""
        assert self.validate(
            "year_or_default_returns_own_year",
            yeared_subject=yeared_subject,
            expected_year=expected_year,
        )


class NoYearOrDefaultReturnsOwnYearMixin(YearOrDefaultReturnsOwnYearMixin, ABC):
    negative_year_or_default_returns_own_year: bool = True


# --- feature: year_default_is_1970 -------------------------------------------------

class YearDefaultIs1970MixinBase(YearedFixturesMixin, ABC):
    """year_or_default() falls back to the documented arbitrary 1970."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "year_default_is_1970":
            subject: YearedComponent = kwargs["yeared_subject"]
            return subject.year_or_default() == 1970
        return super().condition(feature, *args, **kwargs)


class YearDefaultIs1970Mixin(YearDefaultIs1970MixinBase, ABC):
    negative_year_default_is_1970: bool = False

    @pytest.mark.calendar
    def test_year_default_is_1970(self, yeared_subject: YearedComponent) -> None:
        """Year-less subjects default to 1970 (negated when a real year is set)."""
        assert self.validate("year_default_is_1970", yeared_subject=yeared_subject)


class NoYearDefaultIs1970Mixin(YearDefaultIs1970Mixin, ABC):
    negative_year_default_is_1970: bool = True


# --- feature: equal_with_different_year ----------------------------------------------

class EqualWithDifferentYearMixinBase(YearedFixturesMixin, ABC):
    """
    Same component value but different year: __eq__ must take the year into
    account, so test classes always use the *No* variant of this feature.
    """

    @pytest.fixture
    def different_year_subject(self) -> YearedComponent:
        """Same value as `yeared_subject` but constructed with another year."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "equal_with_different_year":
            subject: YearedComponent = kwargs["yeared_subject"]
            other: YearedComponent = kwargs["different_year_subject"]
            # Equality AND matching hashes - both must be False for the No variant.
            return subject == other or hash(subject) == hash(other)
        return super().condition(feature, *args, **kwargs)


class EqualWithDifferentYearMixin(EqualWithDifferentYearMixinBase, ABC):
    negative_equal_with_different_year: bool = False

    @pytest.mark.identity
    @pytest.mark.calendar
    def test_equal_with_different_year(
        self,
        yeared_subject: YearedComponent,
        different_year_subject: YearedComponent,
    ) -> None:
        """Instances differing only by year are distinct in __eq__ and __hash__."""
        assert self.validate(
            "equal_with_different_year",
            yeared_subject=yeared_subject,
            different_year_subject=different_year_subject,
        )


class NoEqualWithDifferentYearMixin(EqualWithDifferentYearMixin, ABC):
    negative_equal_with_different_year: bool = True
