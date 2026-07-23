"""
sku_validator.py

Validates inbound SKU / product-code fields before they enter the
reconciliation pipeline.
"""

import re

# PY3-MIGRATED: re.ASCII added to every pattern using \w/\d/\s. In Python 3 these
# classes are Unicode-aware by default; Python 2 byte-string patterns matched
# ASCII only. re.ASCII preserves the original (ASCII) validation semantics so
# data-entry gating behaves identically after migration. See report review item.
SKU_PATTERN = re.compile(r'^[A-Z]{2}\d{6}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
LOT_CODE_PATTERN = re.compile(r'^\w{4,12}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w semantics
BIN_LOCATION_PATTERN = re.compile(r'^[A-Z]\d{2}-\d{2}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
QUANTITY_TOKEN_PATTERN = re.compile(r'^\d+$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
WHITESPACE_TRIM_PATTERN = re.compile(r'\s+', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \s semantics
DESCRIPTION_ALLOWED_PATTERN = re.compile(r'^[\w\s\-,.]+$')  # PY3-REVIEW: \w/\s left Unicode-aware so descriptions may contain accented text; add re.ASCII if ASCII-only is required


def is_valid_sku(sku):
    return bool(SKU_PATTERN.match(sku))


def is_valid_lot_code(lot_code):
    return bool(LOT_CODE_PATTERN.match(lot_code))


def is_valid_bin_location(bin_location):
    return bool(BIN_LOCATION_PATTERN.match(bin_location))


def normalize_description(description):
    return WHITESPACE_TRIM_PATTERN.sub(' ', description).strip()


def is_valid_quantity_token(token):
    # PY3-REVIEW: str.isdigit() is Unicode-aware in Python 3; the re.ASCII \d
    # regex below backstops it, so the final boolean remains ASCII-only as in Py2.
    if not token.isdigit():
        return False
    return bool(QUANTITY_TOKEN_PATTERN.match(token))


def is_valid_description(description):
    return bool(DESCRIPTION_ALLOWED_PATTERN.match(description))
