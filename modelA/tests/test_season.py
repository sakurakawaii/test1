"""Tests for dateutils/season.py (via the corrected FixedSeason; REPORT.md D1)."""
import pytest
from typing import Any

from dateutils.base import NamedNumericDateComponentBase
from mixins_numeric import PlainNumericComponentMixins
from mixins_named import NamedComponentMixins, ResolvesAliasesMixin, YearedComponentMixins
from helpers import FixedSeason


class TestSeason(
    PlainNumericComponentMixins,
    NamedComponentMixins,
    ResolvesAliasesMixin,
    YearedComponentMixins,
):
    """Season = numeric + naming contracts + 'fall' alias + optional year."""

    # Named components accept strings, so the plain-numeric rejection flips.
    negative_rejects_string_values: bool = True

    @pytest.fixture
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]:
        return FixedSeason

    @pytest.fixture
    def yeared_cls(self) -> type[FixedSeason]:
        return FixedSeason

    @pytest.fixture
    def min_value(self) -> int:
        return 1

    @pytest.fixture
    def max_value(self) -> int:
        return 4

    @pytest.fixture
    def in_range_value(self) -> int:
        return 2

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 3

    @pytest.fixture
    def safe_delta(self) -> int:
        # 2 +/- 1 stays inside 1..4.
        return 1

    @pytest.fixture
    def sample_name(self) -> str:
        return "summer"

    @pytest.fixture
    def sample_name_int(self) -> int:
        return 2

    @pytest.fixture
    def other_name(self) -> str:
        return "winter"

    @pytest.fixture
    def other_name_int(self) -> int:
        return 4

    @pytest.fixture
    def alias_name(self) -> str:
        return "fall"

    @pytest.fixture
    def canonical_name(self) -> str:
        return "autumn"
