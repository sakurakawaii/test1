"""Tests for dateutils/__init__.py - the package's public re-exports.

Note: `duration` is NOT re-exported by the package (see REPORT.md note N1);
the export list below reflects what the __init__ actually promises today.
"""
import pytest
from abc import ABC
from typing import Any

from test_utils import Mixin
import dateutils


class ExportsPublicApiMixinBase(Mixin, ABC):
    """Feature: the package root exposes the component classes."""

    def condition(self, feature: str, *args: Any, **kwargs: Any) -> bool:
        if feature == "exports_public_api":
            expected = (
                "NumericDateComponentBase", "NamedNumericDateComponentBase",
                "Month", "Weekday", "Season", "Hour", "Minute", "Second",
            )
            return all(hasattr(dateutils, name) for name in expected)
        return super().condition(feature, *args, **kwargs)


class ExportsPublicApiMixin(ExportsPublicApiMixinBase, ABC):
    negative_exports_public_api: bool = False

    @pytest.mark.feature_exports
    def test_exports_public_api(self) -> None:
        """All component classes are importable from the package root."""
        assert self.validate("exports_public_api")


class NoExportsPublicApiMixin(ExportsPublicApiMixinBase, ABC):
    negative_exports_public_api: bool = True

    @pytest.mark.feature_exports
    def test_exports_public_api(self) -> None:
        """Negated variant: exports must be missing."""
        assert self.validate("exports_public_api")


class TestPackageExports(ExportsPublicApiMixin):
    """The dateutils package re-exports the component API."""
