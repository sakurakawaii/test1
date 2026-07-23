"""
stock_analytics.py

Demand and count-field analytics for the nightly reconciliation
summary.
"""

from __future__ import division

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
    return total_units_sold / days_in_period


def demand_variance_ratio(peak_day_units, average_daily_units):
    return peak_day_units / average_daily_units


def is_numeric_count_token(token):
    return token.isdigit()
