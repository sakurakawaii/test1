"""
purchase_order_validator.py

Validates purchase-order fields (PO numbers, line item counts, currency
amounts) received from supplier EDI feeds before they are matched
against inbound shipments.

PY3-REVIEW [MEDIUM - Unicode regex/str semantics]: No Python 2 syntax
constructs are present, so no lines were changed. In Python 3 the regex
digit and word classes match Unicode by default, and str.isdigit() accepts
non-ASCII digits; PO/EDI fields are expected to be ASCII, so results differ
only if non-ASCII input reaches these validators. Compile the patterns with
re.ASCII if strict ASCII matching is required.
"""

import re

PO_NUMBER_PATTERN = re.compile(r'^PO-\d{8}$')
LINE_ITEM_COUNT_PATTERN = re.compile(r'^\d{1,4}$')
CURRENCY_AMOUNT_PATTERN = re.compile(r'^\d+\.\d{2}$')
SUPPLIER_REF_PATTERN = re.compile(r'^[\w\-]{3,20}$')


def is_valid_po_number(po_number):
    return bool(PO_NUMBER_PATTERN.match(po_number))


def is_valid_line_item_count(count_str):
    if not count_str.isdigit():
        return False
    return bool(LINE_ITEM_COUNT_PATTERN.match(count_str))


def is_valid_currency_amount(amount_str):
    return bool(CURRENCY_AMOUNT_PATTERN.match(amount_str))


def is_valid_supplier_ref(ref):
    return bool(SUPPLIER_REF_PATTERN.match(ref))
