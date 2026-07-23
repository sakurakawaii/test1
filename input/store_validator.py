"""
store_validator.py

Validates destination store / distribution-center codes on stock
transfer records before they are handed off to the routing layer.
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
