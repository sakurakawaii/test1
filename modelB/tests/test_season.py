"""
Tests for datecomponents/season.py.

The shipped Season has an empty _NAMES list on Python 3.12+ (defect D1, see
REPORT.md and tests/test_rejections.py). `UsableSeason` follows the documented
extension contract to supply the intended names, including the 'fall' alias.
"""
import pytest

from datecomponents.minute import Minute
from datecomponents.season import Season
from tests.mixins.named import NamedComponentMixin, ResolvesAliasMixin
from tests.mixins.numeric import PlainNumericComponentMixin
from tests.mixins.yeared import (
    HasYearMixin,
    NoEqualWithDifferentYearMixin,
    NoYearDefaultIs1970Mixin,
    YearOrDefaultReturnsOwnYearMixin,
)

SEASON_NAMES = ["spring", "summer", "autumn", "winter", "fall"]


class UsableSeason(Season):
    """Season with the names its `SeasonName` alias declares (D1 workaround)."""

    _NAMES = SEASON_NAMES


class TestSeason(PlainNumericComponentMixin, NamedComponentMixin, ResolvesAliasMixin):
    """Season's inherited numeric/named behavior plus the 'fall' alias."""

    @pytest.fixture
    def component_cls(self) -> type[UsableSeason]:
        return UsableSeason

    @pytest.fixture
    def valid_int(self) -> int:
        # 2 = summer (1-based).
        return 2

    @pytest.fixture
    def valid_name(self) -> str:
        return "summer"

    @pytest.fixture
    def add_delta(self) -> int:
        # 2 + 1 = 3 < 4: strictly below _MAX (wrap-around is defective, D2).
        return 1

    @pytest.fixture
    def sub_delta(self) -> int:
        # 2 - 1 = 1 == _MIN: landing on _MIN does not wrap.
        return 1

    @pytest.fixture
    def alias_name(self) -> str:
        return "fall"

    @pytest.fixture
    def canonical_of_alias(self) -> str:
        return "autumn"

    @pytest.fixture
    def other_typed_value(self) -> Minute:
        return Minute(2)


class TestSeasonWithYear(
    HasYearMixin,
    YearOrDefaultReturnsOwnYearMixin,
    NoYearDefaultIs1970Mixin,
    NoEqualWithDifferentYearMixin,
):
    """Year-aware Season behavior with a year supplied."""

    @pytest.fixture
    def yeared_subject(self) -> UsableSeason:
        return UsableSeason("winter", 2024)

    @pytest.fixture
    def expected_year(self) -> int:
        return 2024

    @pytest.fixture
    def different_year_subject(self) -> UsableSeason:
        return UsableSeason("winter", 2025)


class TestSeasonWithoutYear(TestSeasonWithYear):
    """Year-less Season: inherits all tests, flipping the year-driven features."""

    negative_has_year: bool = True
    negative_year_or_default_returns_own_year: bool = True
    negative_year_default_is_1970: bool = False

    @pytest.fixture
    def yeared_subject(self) -> UsableSeason:
        return UsableSeason("winter")
