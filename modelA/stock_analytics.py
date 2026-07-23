"""
stock_analytics.py

Demand and count-field analytics for the nightly reconciliation
summary.
"""

# PY3-MIGRATED: removed `from __future__ import division` (obsolete in
# Python 3). NOTE: because this import WAS present, the `/` operators below
# were already TRUE division in Python 2, and Python 3's default `/` is also
# true division - so behaviour is preserved here. (Contrast with
# inventory_metrics.py, which had no such import and therefore DID change.)

import re

COUNT_FIELD_PATTERN = re.compile(r'^\d+$')
DEMAND_CODE_PATTERN = re.compile(r'^[A-Z]\w{2,5}\d{2}$')


def parse_count_field(s):
    """
    Validates that a raw count field from an upstream feed is a clean
    integer before it is trusted for demand calculations.
    """
    try:
        return int(s)
    except ValueError:
        return None


def is_valid_demand_code(code):
    return bool(DEMAND_CODE_PATTERN.match(code))


def average_daily_demand(total_units_sold, days_in_period):
    # Behaviour preserved: true division in both Py2 (via __future__) and Py3.
    return total_units_sold / days_in_period


def demand_variance_ratio(peak_day_units, average_daily_units):
    # Behaviour preserved: true division in both Py2 (via __future__) and Py3.
    return peak_day_units / average_daily_units


def is_numeric_count_token(token):
    # PY3-REVIEW [MEDIUM - Unicode]: str.isdigit() matches non-ASCII digits in
    # Python 3; if upstream feeds can contain non-ASCII numerals this returns
    # True where Python 2 returned False. Harmless for ASCII-only feeds.
    return token.isdigit()
