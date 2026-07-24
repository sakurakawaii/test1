"""Tests for dateutils/base.py, run against minimal local subclasses.

Subclassing with `_MIN`/`_MAX`/`_NAMES` is the documented public extension
API of both base classes, so these tests pin the base contract independently
of the shipped concrete components.
"""
import pytest
from typing import Any

from dateutils.base import NumericDateComponentBase, NamedNumericDateComponentBase
from mixins_numeric import PlainNumericComponentMixins
from mixins_named import NamedComponentMixins, ResolvesAliasesMixin


class Dozen(NumericDateComponentBase):
    """A minimal plain numeric component used only by these tests."""
    _MIN = 1
    _MAX = 12


class Coin(NamedNumericDateComponentBase[str]):
    """A minimal named component with an alias, used only by these tests."""
    _NAMES = ["heads", "tails", "edge", "rim", "obverse"]  # "obverse" filters out (alias)
    _MIN = 0
    _MAX = 3
    _ALIASES = {"obverse": "heads"}


class TestNumericDateComponentBase(PlainNumericComponentMixins):
    """The plain-numeric contract holds for any minimal subclass."""

    @pytest.fixture
    def component_cls(self) -> type[NumericDateComponentBase]:
        return Dozen

    @pytest.fixture
    def min_value(self) -> int:
        return 1

    @pytest.fixture
    def max_value(self) -> int:
        return 12

    @pytest.fixture
    def in_range_value(self) -> int:
        return 6

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 9

    @pytest.fixture
    def safe_delta(self) -> int:
        # 6 +/- 3 stays inside 1..12.
        return 3

    @pytest.fixture
    def sample_name(self) -> str:
        return "half"


class TestNamedNumericDateComponentBase(
    PlainNumericComponentMixins,
    NamedComponentMixins,
    ResolvesAliasesMixin,
):
    """The named contract (incl. __init_subclass__ alias filtering) holds for
    any minimal subclass that supplies names and aliases."""

    # Named components accept strings, so the plain-numeric rejection flips.
    negative_rejects_string_values: bool = True

    @pytest.fixture
    def component_cls(self) -> type[NamedNumericDateComponentBase[Any]]:
        return Coin

    @pytest.fixture
    def min_value(self) -> int:
        return 0

    @pytest.fixture
    def max_value(self) -> int:
        return 3

    @pytest.fixture
    def in_range_value(self) -> int:
        return 1

    @pytest.fixture
    def other_in_range_value(self) -> int:
        return 2

    @pytest.fixture
    def safe_delta(self) -> int:
        # 1 +/- 1 stays inside 0..3 and clear of the defective _MAX edge (D2).
        return 1

    @pytest.fixture
    def sample_name(self) -> str:
        return "heads"

    @pytest.fixture
    def sample_name_int(self) -> int:
        return 0

    @pytest.fixture
    def other_name(self) -> str:
        return "tails"

    @pytest.fixture
    def other_name_int(self) -> int:
        return 1

    @pytest.fixture
    def alias_name(self) -> str:
        return "obverse"

    @pytest.fixture
    def canonical_name(self) -> str:
        return "heads"
