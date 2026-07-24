"""Tests for dateutils/minute.py — a plain numeric component (0-59)."""
import pytest
from dateutils.minute import Minute
from dateutils.base import NumericDateComponentBase
from mixins_numeric import PlainNumericComponentMixins


class TestMinute(PlainNumericComponentMixins):
    """Minute satisfies the full plain-numeric component contract."""

    @pytest.fixture
    def component_cls(self) -> type[NumericDateComponentBase]:
        return Minute

    @pytest.fixture
    def min_value(self) -> int:
        return 0

    @pytest.fixture
    def max_value(self) -> int:
        return 59

    @pytest.fixture
    def in_range_value(self) -> int:
        return 30

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 45

    @pytest.fixture
    def safe_delta(self) -> int:
        # 30 +/- 10 stays inside 0..59, so no wrap-around is triggered.
        return 10

    @pytest.fixture
    def sample_name(self) -> str:
        # Plain numeric components have no names; any string must be rejected.
        return "thirty"
