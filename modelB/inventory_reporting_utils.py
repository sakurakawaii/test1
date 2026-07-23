"""
inventory_reporting_utils.py

Parses and formats fixed-width and semi-structured inventory report
lines produced by the warehouse management system for nightly
reconciliation summaries.
"""

import re

# PY3-MIGRATED: re.ASCII preserves Python 2 ASCII-only \w/\d/\s semantics for
# fixed-width report parsing (Python 3 makes these classes Unicode-aware by
# default). See report review item.
REPORT_LINE_PATTERN = re.compile(r'^(\w+)\s+(\d+)\s+(\d+\.\d{2})$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w/\d/\s semantics
HEADER_PATTERN = re.compile(r'^-{3,}\s*\w+\s*-{3,}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w/\s semantics
NUMERIC_FIELD_PATTERN = re.compile(r'\d+', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics
TRAILING_SPACE_PATTERN = re.compile(r'\s+$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \s semantics


def parse_report_line(line):
    match = REPORT_LINE_PATTERN.match(line.strip())
    if not match:
        return None
    sku, quantity, value = match.groups()
    # PY3-REVIEW: str.isdigit() is Unicode-aware in Python 3; the re.ASCII \d
    # group above backstops it, so only ASCII digits reach this check as in Py2.
    if not quantity.isdigit():
        return None
    return {'sku': sku, 'quantity': int(quantity), 'value': float(value)}


def is_section_header(line):
    return bool(HEADER_PATTERN.match(line))


def extract_numeric_fields(line):
    # PY3-REVIEW: findall() returns a list in both Python 2 and 3 (no iterator
    # change here); callers that index/len the result remain safe.
    return NUMERIC_FIELD_PATTERN.findall(line)


def strip_trailing_space(line):
    return TRAILING_SPACE_PATTERN.sub('', line)
