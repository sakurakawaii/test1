"""
store_validator.py

Validates destination store / distribution-center codes on stock
transfer records before they are handed off to the routing layer.

PY3-REVIEW [MEDIUM - Unicode regex/str semantics]: No Python 2 syntax
constructs are present, so no lines were changed. In Python 3 str.isalpha()
and the regex word/digit classes are Unicode-aware; store/DC/region codes
are expected to be ASCII, so results differ only if non-ASCII input reaches
these validators. Compile the patterns with re.ASCII for strict ASCII.
"""

import re

STORE_CODE_PATTERN = re.compile(r'^ST-\d{4}$')
DC_CODE_PATTERN = re.compile(r'^DC-[A-Z]{2}\d{2}$')
REGION_CODE_PATTERN = re.compile(r'^[A-Z]{2,3}$')
TRANSFER_REF_PATTERN = re.compile(r'^\w{6,16}$')


def is_valid_store_code(code):
    return bool(STORE_CODE_PATTERN.match(code))


def is_valid_dc_code(code):
    return bool(DC_CODE_PATTERN.match(code))


def is_valid_region_code(code):
    return code.isalpha() and bool(REGION_CODE_PATTERN.match(code))


def is_valid_transfer_ref(ref):
    return bool(TRANSFER_REF_PATTERN.match(ref))
