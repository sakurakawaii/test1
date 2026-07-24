"""
Tests for datecomponents/weekday.py.

The shipped Weekday has an empty _NAMES list on Python 3.12+ (defect D1, see
REPORT.md and tests/test_rejections.py), so it cannot be instantiated at all.
`UsableWeekday` below follows the documented extension contract to supply the
intended names, letting us verify all of Weekday's inherited behavior.
"""
import pytest

from datecomponents.minute import Minute
from datecomponents.weekday import Weekday
from tests.mixins.named import NamedComponentMixin
from tests.mixins.numeric import PlainNumericComponentMixin

WEEKDAY_NAMES = [
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
]


class UsableWeekday(Weekday):
    """Weekday with the names its `WeekdayName` alias declares (D1 workaround)."""

    _NAMES = WEEKDAY_NAMES


class TestWeekday(PlainNumericComponentMixin, NamedComponentMixin):
    """Weekday is a named component over 0-6, Monday first (datetime parity)."""

    @pytest.fixture
    def component_cls(self) -> type[UsableWeekday]:
        return UsableWeekday

    @pytest.fixture
    def valid_int(self) -> int:
        # 3 = thursday (0-based, matching datetime.date.weekday()).
        return 3

    @pytest.fixture
    def valid_name(self) -> str:
        return "thursday"

    @pytest.fixture
    def add_delta(self) -> int:
        # 3 + 2 = 5 < 6: stays strictly below _MAX (wrap-around is defective, D2).
        return 2

    @pytest.fixture
    def sub_delta(self) -> int:
        # 3 - 3 = 0 == _MIN: landing on _MIN does not wrap.
        return 3

    @pytest.fixture
    def other_typed_value(self) -> Minute:
        return Minute(3)
