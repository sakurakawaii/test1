"""
inventory_reporting_utils.py

Parses and formats fixed-width and semi-structured inventory report
lines produced by the warehouse management system for nightly
reconciliation summaries.
"""

import re

REPORT_LINE_PATTERN = re.compile(r'^(\w+)\s+(\d+)\s+(\d+\.\d{2})$')
HEADER_PATTERN = re.compile(r'^-{3,}\s*\w+\s*-{3,}$')
NUMERIC_FIELD_PATTERN = re.compile(r'\d+')
TRAILING_SPACE_PATTERN = re.compile(r'\s+$')


def parse_report_line(line):
    match = REPORT_LINE_PATTERN.match(line.strip())
    if not match:
        return None
    sku, quantity, value = match.groups()
    if not quantity.isdigit():
        return None
    return {'sku': sku, 'quantity': int(quantity), 'value': float(value)}


def is_section_header(line):
    return bool(HEADER_PATTERN.match(line))


def extract_numeric_fields(line):
    return NUMERIC_FIELD_PATTERN.findall(line)


def strip_trailing_space(line):
    return TRAILING_SPACE_PATTERN.sub('', line)
