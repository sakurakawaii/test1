"""Tests for dateutils/hour.py (via the corrected FixedHour; see REPORT.md D1)."""
import pytest
from abc import ABC
from typing import Any

from test_utils import Mixin
from dateutils.base import NamedNumericDateComponentBase
from mixins_numeric import PlainNumericComponentMixins
from mixins_named import NamedComponentMixins, ResolvesAliasesMixin
from helpers import FixedHour


class ConvertsClockFormatsMixinBase(Mixin, ABC):
    """Feature: Hour converts between 24h ints and 12h names."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "converts_clock_formats":
            return (
                FixedHour(13).to_24h() == 13
                and FixedHour(13).to_12h() == "1pm"
                and FixedHour("11pm").to_24h() == 23
                and FixedHour(0).to_12h() == "12am"
                # the special aliases normalize to standard 12h names
                and FixedHour("noon").to_12h() == "12pm"
            )
        return super().condition(feature, *args, **kwargs)


class ConvertsClockFormatsMixin(ConvertsClockFormatsMixinBase, ABC):
    negative_converts_clock_formats: bool = False

    @pytest.mark.feature_clock_format
    def test_converts_clock_formats(self) -> None:
        """to_24h/to_12h round-trip between int hours and 12h names."""
        assert self.validate("converts_clock_formats")


class NoConvertsClockFormatsMixin(ConvertsClockFormatsMixinBase, ABC):
    negative_converts_clock_formats: bool = True

    @pytest.mark.feature_clock_format
    def test_converts_clock_formats(self) -> None:
        """Negated variant: clock conversion must not work."""
        assert self.validate("converts_clock_formats")


class TestHour(
    PlainNumericComponentMixins,
    NamedComponentMixins,
    ResolvesAliasesMixin,
    ConvertsClockFormatsMixin,
):
    """Hour = numeric + naming contracts + aliases + clock conversions."""

    # Named components accept strings, so the plain-numeric rejection flips.
    negative_rejects_string_values: bool = True

    @pytest.fixture
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]:
        return FixedHour

    @pytest.fixture
    def min_value(self) -> int:
        return 0

    @pytest.fixture
    def max_value(self) -> int:
        return 23

    @pytest.fixture
    def in_range_value(self) -> int:
        return 10

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 15

    @pytest.fixture
    def safe_delta(self) -> int:
        # 10 +/- 5 stays inside 0..23.
        return 5

    @pytest.fixture
    def sample_name(self) -> str:
        return "3pm"

    @pytest.fixture
    def sample_name_int(self) -> int:
        return 15

    @pytest.fixture
    def other_name(self) -> str:
        return "7am"

    @pytest.fixture
    def other_name_int(self) -> int:
        return 7

    @pytest.fixture
    def alias_name(self) -> str:
        return "midnight"

    @pytest.fixture
    def canonical_name(self) -> str:
        return "12am"
