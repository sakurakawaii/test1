"""Tests for datecomponents/minute.py (Minute: 0-59)."""
import pytest

from datecomponents.minute import Minute
from datecomponents.second import Second
from tests.mixins.numeric import (
    FailsArgtypeWithNonNumericMixin,
    PlainNumericComponentMixin,
)


class TestMinute(PlainNumericComponentMixin, FailsArgtypeWithNonNumericMixin):
    """Minute supports every plain numeric component feature."""

    @pytest.fixture
    def component_cls(self) -> type[Minute]:
        return Minute

    @pytest.fixture
    def valid_int(self) -> int:
        # 30 is comfortably inside 0-59.
        return 30

    @pytest.fixture
    def add_delta(self) -> int:
        # 30 + 20 = 50 < 59, so no wrap-around is involved.
        return 20

    @pytest.fixture
    def sub_delta(self) -> int:
        # 30 - 25 = 5 > 0, so no wrap-around is involved.
        return 25

    @pytest.fixture
    def other_typed_value(self) -> Second:
        # Same numeric value, different component type: must not compare equal.
        return Second(30)
