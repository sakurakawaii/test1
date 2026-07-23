"""
purchase_order_validator.py

Validates purchase-order fields (PO numbers, line item counts, currency
amounts) received from supplier EDI feeds before they are matched
against inbound shipments.
"""

import re

# PY3-MIGRATED: re.ASCII preserves Python 2 ASCII-only \d/\w semantics (Python 3
# makes these classes Unicode-aware by default). See report review item.
PO_NUMBER_PATTERN = re.compile(r'^PO-\d{8}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
LINE_ITEM_COUNT_PATTERN = re.compile(r'^\d{1,4}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
CURRENCY_AMOUNT_PATTERN = re.compile(r'^\d+\.\d{2}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
SUPPLIER_REF_PATTERN = re.compile(r'^[\w\-]{3,20}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w semantics


def is_valid_po_number(po_number):
    return bool(PO_NUMBER_PATTERN.match(po_number))


def is_valid_line_item_count(count_str):
    # PY3-REVIEW: str.isdigit() is Unicode-aware in Python 3; the re.ASCII \d
    # regex backstops it so the final boolean stays ASCII-only as in Python 2.
    if not count_str.isdigit():
        return False
    return bool(LINE_ITEM_COUNT_PATTERN.match(count_str))


def is_valid_currency_amount(amount_str):
    return bool(CURRENCY_AMOUNT_PATTERN.match(amount_str))


def is_valid_supplier_ref(ref):
    return bool(SUPPLIER_REF_PATTERN.match(ref))
