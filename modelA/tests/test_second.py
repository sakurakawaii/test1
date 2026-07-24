"""Tests for dateutils/second.py — behaviorally identical to Minute.

TestSecond inherits every test from TestMinute unchanged (no negations:
nothing is overridden in the source), only the class under test swaps.
"""
import pytest
from dateutils.second import Second
from dateutils.base import NumericDateComponentBase
from test_minute import TestMinute


class TestSecond(TestMinute):
    """Second satisfies the same contract as Minute (0-59)."""

    @pytest.fixture
    def component_cls(self) -> type[NumericDateComponentBase]:
        return Second
