"""
Tests for datecomponents/second.py (Second: 0-59).

TestSecond subclasses TestMinute: Second has the exact same contract, so it
inherits the full feature suite and only swaps the fixtures. No features are
overridden, hence no `negative_*` flags are flipped here.
"""
import pytest

from datecomponents.minute import Minute
from datecomponents.second import Second
from tests.test_minute import TestMinute


class TestSecond(TestMinute):
    """Second inherits all Minute tests, re-pointed at the Second class."""

    @pytest.fixture
    def component_cls(self) -> type[Second]:
        return Second

    @pytest.fixture
    def other_typed_value(self) -> Minute:
        # The cross-type value flips direction: a Minute is foreign to Second.
        return Minute(30)
