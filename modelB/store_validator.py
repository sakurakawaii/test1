"""
store_validator.py

Validates destination store / distribution-center codes on stock
transfer records before they are handed off to the routing layer.
"""

import re

# PY3-MIGRATED: re.ASCII preserves Python 2 ASCII-only \d/\w semantics (Python 3
# makes these classes Unicode-aware by default). See report review item.
STORE_CODE_PATTERN = re.compile(r'^ST-\d{4}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
DC_CODE_PATTERN = re.compile(r'^DC-[A-Z]{2}\d{2}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
REGION_CODE_PATTERN = re.compile(r'^[A-Z]{2,3}$', re.ASCII)  # PY3-MIGRATED: re.ASCII (literal ASCII range; flag kept for consistency)
TRANSFER_REF_PATTERN = re.compile(r'^\w{6,16}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w semantics


def is_valid_store_code(code):
    return bool(STORE_CODE_PATTERN.match(code))


def is_valid_dc_code(code):
    return bool(DC_CODE_PATTERN.match(code))


def is_valid_region_code(code):
    # PY3-REVIEW: str.isalpha() is Unicode-aware in Python 3 (accented letters
    # return True); the re.ASCII [A-Z] regex backstops it so the result stays
    # ASCII-only as in Python 2.
    return code.isalpha() and bool(REGION_CODE_PATTERN.match(code))


def is_valid_transfer_ref(ref):
    return bool(TRANSFER_REF_PATTERN.match(ref))
