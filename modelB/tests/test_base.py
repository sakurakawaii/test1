"""
Tests for datecomponents/base.py, exercised through the documented public
extension contract: "Subclasses must define _MIN and _MAX" (and _NAMES for the
named base). The locally defined subclasses below are well-formed extensions,
so these tests pin down the base-class logic itself independently of the
shipped concrete components (which are defective - see REPORT.md D1).
"""
import pytest

from datecomponents.base import (
    NamedNumericDateComponentBase,
    NumericDateComponentBase,
)
from tests.mixins.named import NamedComponentMixin, ResolvesAliasMixin
from tests.mixins.numeric import (
    FailsArgtypeWithNonNumericMixin,
    PlainNumericComponentMixin,
)


class DiceFace(NumericDateComponentBase):
    """A minimal, contract-conforming plain component (1-6)."""

    _MIN = 1
    _MAX = 6


class Quarter(NamedNumericDateComponentBase[str]):
    """A minimal, contract-conforming named component with an alias (1-4)."""

    _NAMES = ["first", "second", "third", "fourth", "q4"]
    _MIN = 1
    _MAX = 4
    _ALIASES = {"q4": "fourth"}


class TestNumericDateComponentBase(
    PlainNumericComponentMixin, FailsArgtypeWithNonNumericMixin
):
    """The plain numeric base provides the full numeric feature set."""

    @pytest.fixture
    def component_cls(self) -> type[DiceFace]:
        return DiceFace

    @pytest.fixture
    def valid_int(self) -> int:
        return 3

    @pytest.fixture
    def add_delta(self) -> int:
        # 3 + 2 = 5 < 6: stays below _MAX (wrap-around is defective, D2).
        return 2

    @pytest.fixture
    def sub_delta(self) -> int:
        # 3 - 1 = 2 > 1: stays above _MIN.
        return 1

    @pytest.fixture
    def other_typed_value(self) -> Quarter:
        return Quarter(3)


class TestNamedNumericDateComponentBase(
    PlainNumericComponentMixin, NamedComponentMixin, ResolvesAliasMixin
):
    """The named base adds name handling and alias resolution on top."""

    @pytest.fixture
    def component_cls(self) -> type[Quarter]:
        return Quarter

    @pytest.fixture
    def valid_int(self) -> int:
        return 2

    @pytest.fixture
    def valid_name(self) -> str:
        return "second"

    @pytest.fixture
    def add_delta(self) -> int:
        # 2 + 1 = 3 < 4: stays strictly below _MAX (wrap-around is defective, D2).
        return 1

    @pytest.fixture
    def sub_delta(self) -> int:
        # 2 - 1 = 1 == _MIN: landing on _MIN does not wrap.
        return 1

    @pytest.fixture
    def alias_name(self) -> str:
        return "q4"

    @pytest.fixture
    def canonical_of_alias(self) -> str:
        return "fourth"

    @pytest.fixture
    def other_typed_value(self) -> DiceFace:
        return DiceFace(2)
