"""
stock_analytics.py

Demand and count-field analytics for the nightly reconciliation
summary.
"""

# PY3-MIGRATED: removed `from __future__ import division` (obsolete in Python 3).
# Verified: this module already used true division in Python 2 via that import,
# and Python 3 `/` is true division, so division behavior is UNCHANGED here.

import re

COUNT_FIELD_PATTERN = re.compile(r'^\d+$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d (ASCII-only) semantics
DEMAND_CODE_PATTERN = re.compile(r'^[A-Z]\w{2,5}\d{2}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w/\d semantics


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
    # Behavior preserved: true division under both Python 2 (__future__) and Python 3.
    return total_units_sold / days_in_period


def demand_variance_ratio(peak_day_units, average_daily_units):
    # Behavior preserved: true division under both Python 2 (__future__) and Python 3.
    return peak_day_units / average_daily_units


def is_numeric_count_token(token):
    # PY3-REVIEW: str.isdigit() is Unicode-aware in Python 3 (e.g. Arabic-Indic
    # digits return True) whereas Python 2 byte strings were ASCII-only. If this
    # token can originate from non-ASCII input, add an explicit ASCII check.
    return token.isdigit()
