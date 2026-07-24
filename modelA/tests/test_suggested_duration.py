"""
SUGGESTED features for Duration (see REPORT.md, "Suggested features").
All marked `suggested_feature` + `xfail`: they are acknowledged as currently
failing because the features are not implemented yet.
"""
import pytest
from abc import ABC
from typing import Any

from test_utils import Mixin
from dateutils.duration import Duration


xfail_missing = pytest.mark.xfail(reason="suggested feature not implemented yet")


# S6 --------------------------------------------------------------------------
class ConvertsTotalUnitsMixinBase(Mixin, ABC):
    """Suggested: total_minutes()/total_hours()/total_days() companions to
    total_seconds(), mirroring common timedelta usage."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "converts_total_units":
            d = Duration(hours=3)
            return (
                d.total_minutes() == 180  # type: ignore[attr-defined]
                and d.total_hours() == 3  # type: ignore[attr-defined]
                and Duration(weeks=2).total_days() == 14  # type: ignore[attr-defined]
            )
        return super().condition(feature, *args, **kwargs)


class ConvertsTotalUnitsMixin(ConvertsTotalUnitsMixinBase, ABC):
    negative_converts_total_units: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_duration_total
    def test_converts_total_units(self) -> None:
        """Totals should be available in minutes/hours/days too."""
        assert self.validate("converts_total_units")


class NoConvertsTotalUnitsMixin(ConvertsTotalUnitsMixinBase, ABC):
    negative_converts_total_units: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_duration_total
    def test_converts_total_units(self) -> None:
        """Negated variant."""
        assert self.validate("converts_total_units")


@xfail_missing
class TestDurationTotalUnits(ConvertsTotalUnitsMixin):
    """S6: Duration.total_minutes / total_hours / total_days should exist."""


# S7 --------------------------------------------------------------------------
class ParsesIso8601MixinBase(Mixin, ABC):
    """Suggested: Duration.from_iso8601("P1DT2H30M") parsing - very common
    for API-facing backend services exchanging durations as strings."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "parses_iso8601":
            parsed = Duration.from_iso8601("PT1H30M")  # type: ignore[attr-defined]
            return parsed == Duration(hours=1, minutes=30)
        return super().condition(feature, *args, **kwargs)


class ParsesIso8601Mixin(ParsesIso8601MixinBase, ABC):
    negative_parses_iso8601: bool = False

    @pytest.mark.suggested_feature
    @pytest.mark.feature_duration_construction
    def test_parses_iso8601(self) -> None:
        """ISO 8601 duration strings should parse into Durations."""
        assert self.validate("parses_iso8601")


class NoParsesIso8601Mixin(ParsesIso8601MixinBase, ABC):
    negative_parses_iso8601: bool = True

    @pytest.mark.suggested_feature
    @pytest.mark.feature_duration_construction
    def test_parses_iso8601(self) -> None:
        """Negated variant."""
        assert self.validate("parses_iso8601")


@xfail_missing
class TestDurationIso8601(ParsesIso8601Mixin):
    """S7: Duration.from_iso8601 should exist."""
