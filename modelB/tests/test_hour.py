"""
Tests for datecomponents/hour.py.

The shipped Hour has an empty _NAMES list on Python 3.12+ (defect D1, see
REPORT.md and tests/test_rejections.py). `UsableHour` follows the documented
extension contract to supply the intended names so Hour's own conversion
methods and aliases can be verified.
"""
from abc import ABC
from typing import Any

import pytest

from datecomponents.hour import Hour
from datecomponents.minute import Minute
from tests.mixins.named import NamedComponentMixin, ResolvesAliasMixin
from tests.mixins.numeric import ComponentFixturesMixin, PlainNumericComponentMixin

HOUR_NAMES = [
    "12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am",
    "8am", "9am", "10am", "11am",
    "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm",
    "8pm", "9pm", "10pm", "11pm",
    # The special names are filtered back out by __init_subclass__ because
    # they are registered as aliases; listing them mirrors the shipped code.
    "midnight", "noon",
]


class UsableHour(Hour):
    """Hour with the names its `HourName` alias declares (D1 workaround)."""

    _NAMES = HOUR_NAMES


# --- feature: converts_between_12h_and_24h (Hour-specific) ---------------------

class ConvertsBetween12hAnd24hMixinBase(ComponentFixturesMixin, ABC):
    """to_24h mirrors int_id and to_12h yields the am/pm name."""

    @pytest.fixture
    def expected_12h(self) -> str:
        """The 12h name matching `valid_int`."""
        raise NotImplementedError

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "converts_between_12h_and_24h":
            component_cls: type[Hour] = kwargs["component_cls"]
            valid_int: int = kwargs["valid_int"]
            expected_12h: str = kwargs["expected_12h"]
            subject = component_cls(valid_int)
            return subject.to_24h() == valid_int and subject.to_12h() == expected_12h
        return super().condition(feature, *args, **kwargs)


class ConvertsBetween12hAnd24hMixin(ConvertsBetween12hAnd24hMixinBase, ABC):
    negative_converts_between_12h_and_24h: bool = False

    @pytest.mark.conversion
    def test_converts_between_12h_and_24h(
        self, component_cls: type[Hour], valid_int: int, expected_12h: str
    ) -> None:
        """An Hour reports both its 24h int and its 12h am/pm name."""
        assert self.validate(
            "converts_between_12h_and_24h",
            component_cls=component_cls,
            valid_int=valid_int,
            expected_12h=expected_12h,
        )


class NoConvertsBetween12hAnd24hMixin(ConvertsBetween12hAnd24hMixin, ABC):
    negative_converts_between_12h_and_24h: bool = True


class TestHour(
    PlainNumericComponentMixin,
    NamedComponentMixin,
    ResolvesAliasMixin,
    ConvertsBetween12hAnd24hMixin,
):
    """Hour: 0-23 with 12h names plus 'midnight'/'noon' aliases."""

    @pytest.fixture
    def component_cls(self) -> type[UsableHour]:
        return UsableHour

    @pytest.fixture
    def valid_int(self) -> int:
        # 13 = "1pm".
        return 13

    @pytest.fixture
    def valid_name(self) -> str:
        return "1pm"

    @pytest.fixture
    def expected_12h(self) -> str:
        return "1pm"

    @pytest.fixture
    def add_delta(self) -> int:
        # 13 + 9 = 22 < 23: strictly below _MAX (wrap-around is defective, D2).
        return 9

    @pytest.fixture
    def sub_delta(self) -> int:
        # 13 - 13 = 0 == _MIN: landing on _MIN does not wrap.
        return 13

    @pytest.fixture
    def alias_name(self) -> str:
        return "noon"

    @pytest.fixture
    def canonical_of_alias(self) -> str:
        return "12pm"

    @pytest.fixture
    def other_typed_value(self) -> Minute:
        return Minute(13)
