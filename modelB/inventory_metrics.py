"""
inventory_metrics.py

Computes rollup figures used to drive nightly stockout, fill-rate,
and turnover alerts, compared against the threshold constants below.
"""

import re

# PY3-MIGRATED: re.ASCII pins \w/\d to ASCII. In Python 3 these classes are
# Unicode-aware by default; Python 2 (byte-string patterns) matched ASCII only.
# re.ASCII preserves the original validation semantics for these structured IDs.
METRIC_ID_PATTERN = re.compile(r'^[a-z_]+\.\w+$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w semantics
THRESHOLD_TOKEN_PATTERN = re.compile(r'^\d+(\.\d+)?$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d semantics

STOCKOUT_WARNING_LEVEL = 1
STOCKOUT_CRITICAL_LEVEL = 2
FILL_RATE_FLOOR = 0.95
TURNOVER_FLOOR = 0.80
FORECAST_ACCURACY_FLOOR = 0.90


def is_valid_metric_id(metric_id):
    return bool(METRIC_ID_PATTERN.match(metric_id))


def is_valid_threshold_token(token):
    if not token.replace('.', '', 1).isdigit():
        return False
    return bool(THRESHOLD_TOKEN_PATTERN.match(token))


def count_stockout_events(actual_stockouts, allowed_stockout_budget):
    """
    Returns stockout events against the allowed stockout budget,
    compared against STOCKOUT_WARNING_LEVEL / STOCKOUT_CRITICAL_LEVEL.
    """
    # PY3-REVIEW: `/` was INTEGER division in Python 2 (no __future__ division here).
    # In Python 3 it is TRUE division, so the return type changes int -> float and
    # the numeric result differs (e.g. 3/2 was 1, now 1.5). Kept as a ratio/multiple
    # because it is compared against fractional-capable levels. Confirm downstream
    # alert logic and any historical baselines tolerate float output. (See report MR.)
    return actual_stockouts / allowed_stockout_budget


def count_reorder_multiples(triggered_reorders, expected_reorders):
    """
    Returns triggered reorders as a multiple of the expected/forecast
    reorder count for the period.
    """
    # PY3-REVIEW: Python 2 integer division -> Python 3 true division. Return type
    # int -> float and value differs. "Multiple" is semantically fractional, so
    # true division is retained; verify no caller uses this as an int index/key.
    return triggered_reorders / expected_reorders


def compute_fill_rate_ratio(units_shipped, units_ordered):
    # PY3-REVIEW: Python 2 integer division -> Python 3 true division. A fill rate
    # compared against FILL_RATE_FLOOR=0.95 is inherently fractional, so true
    # division is the correct behavior, but it differs from the Python 2 output
    # (which floored to 0/1). Return type int -> float. Verify downstream consumers.
    return units_shipped / units_ordered


def compute_turnover_ratio(units_sold, average_inventory_on_hand):
    # PY3-REVIEW: Python 2 integer division -> Python 3 true division (compared
    # against TURNOVER_FLOOR=0.80). Return type int -> float; value differs.
    return units_sold / average_inventory_on_hand


def compute_forecast_accuracy_ratio(correct_forecasts, total_forecasts):
    # PY3-REVIEW: Python 2 integer division -> Python 3 true division (compared
    # against FORECAST_ACCURACY_FLOOR=0.90). Return type int -> float; value differs.
    return correct_forecasts / total_forecasts
