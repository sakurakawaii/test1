"""
sku_validator.py

Validates inbound SKU / product-code fields before they enter the
reconciliation pipeline.

PY3-REVIEW [MEDIUM - Unicode regex/str semantics]: No Python 2 syntax
constructs are present, so no lines were changed. However, in Python 3 the
regex digit and word classes match Unicode by default (not just ASCII), and
str.isdigit() returns True for non-ASCII digits. SKU/lot/bin codes are
expected to be ASCII; if any upstream feed can deliver non-ASCII text,
validation results will differ from Python 2. If strict ASCII is required,
compile the patterns with re.ASCII.
"""

import re

SKU_PATTERN = re.compile(r'^[A-Z]{2}\d{6}$')
LOT_CODE_PATTERN = re.compile(r'^\w{4,12}$')
BIN_LOCATION_PATTERN = re.compile(r'^[A-Z]\d{2}-\d{2}$')
QUANTITY_TOKEN_PATTERN = re.compile(r'^\d+$')
WHITESPACE_TRIM_PATTERN = re.compile(r'\s+')
DESCRIPTION_ALLOWED_PATTERN = re.compile(r'^[\w\s\-,.]+$')


def is_valid_sku(sku):
    return bool(SKU_PATTERN.match(sku))


def is_valid_lot_code(lot_code):
    return bool(LOT_CODE_PATTERN.match(lot_code))


def is_valid_bin_location(bin_location):
    return bool(BIN_LOCATION_PATTERN.match(bin_location))


def normalize_description(description):
    return WHITESPACE_TRIM_PATTERN.sub(' ', description).strip()


def is_valid_quantity_token(token):
    if not token.isdigit():
        return False
    return bool(QUANTITY_TOKEN_PATTERN.match(token))


def is_valid_description(description):
    return bool(DESCRIPTION_ALLOWED_PATTERN.match(description))
