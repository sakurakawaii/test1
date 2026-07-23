"""
inventory_metrics.py

Computes rollup figures used to drive nightly stockout, fill-rate,
and turnover alerts, compared against the threshold constants below.
"""

import re

METRIC_ID_PATTERN = re.compile(r'^[a-z_]+\.\w+$')
THRESHOLD_TOKEN_PATTERN = re.compile(r'^\d+(\.\d+)?$')

STOCKOUT_WARNING_LEVEL = 1
STOCKOUT_CRITICAL_LEVEL = 2
FILL_RATE_FLOOR = 0.95
TURNOVER_FLOOR = 0.80
FORECAST_ACCURACY_FLOOR = 0.90


def is_valid_metric_id(metric_id):
    return bool(METRIC_ID_PATTERN.match(metric_id))


def is_valid_threshold_token(token):
    # PY3-REVIEW [MEDIUM - Unicode]: str.isdigit() and the regex \d now match
    # non-ASCII digits in Python 3 (e.g. Arabic-Indic numerals). If threshold
    # tokens can contain non-ASCII input this accepts values Python 2 rejected.
    if not token.replace('.', '', 1).isdigit():
        return False
    return bool(THRESHOLD_TOKEN_PATTERN.match(token))


def count_stockout_events(actual_stockouts, allowed_stockout_budget):
    """
    Returns stockout events against the allowed stockout budget,
    compared against STOCKOUT_WARNING_LEVEL / STOCKOUT_CRITICAL_LEVEL.
    """
    # PY3-REVIEW [CRITICAL - silent numeric drift]: this module has NO
    # `from __future__ import division`, so in Python 2 this was FLOOR
    # division (int/int -> int). In Python 3 `/` is true division. The sole
    # caller (inventory_core.run) passes integers and stores the result as
    # 'stockout_ratio', so true division is the intended behaviour - but the
    # nightly output VALUE changes (e.g. 3/10 was 0 in Py2, is 0.3 now).
    # Confirm with ops which behaviour the stockout alert thresholds expect.
    return actual_stockouts / allowed_stockout_budget


def count_reorder_multiples(triggered_reorders, expected_reorders):
    """
    Returns triggered reorders as a multiple of the expected/forecast
    reorder count for the period.
    """
    # PY3-REVIEW [CRITICAL - silent numeric drift]: floor division in Python 2
    # (no __future__ division), true division in Python 3. No caller in this
    # submission. "multiple" implies a fractional result is intended, so `/`
    # is kept, but output changes vs. production - confirm intended semantics.
    return triggered_reorders / expected_reorders


def compute_fill_rate_ratio(units_shipped, units_ordered):
    # PY3-REVIEW [CRITICAL - silent numeric drift]: floor division in Python 2
    # (no __future__ division). Compared downstream against FILL_RATE_FLOOR
    # (0.95), which only makes sense for a fractional ratio, so true division
    # is the clear design intent and Python 2 was effectively a latent bug
    # (fill_rate was always 0 or 1). Python 3 now yields the correct ratio,
    # but nightly fill_rate values WILL change - requires ops/Finance sign-off.
    return units_shipped / units_ordered


def compute_turnover_ratio(units_sold, average_inventory_on_hand):
    # PY3-REVIEW [CRITICAL - silent numeric drift]: floor division in Python 2.
    # Compared against TURNOVER_FLOOR (0.80); true division is intended and
    # kept, but output changes vs. production (Py2 floored to 0/1).
    return units_sold / average_inventory_on_hand


def compute_forecast_accuracy_ratio(correct_forecasts, total_forecasts):
    # PY3-REVIEW [CRITICAL - silent numeric drift]: floor division in Python 2.
    # Compared against FORECAST_ACCURACY_FLOOR (0.90); true division intended
    # and kept, but output changes vs. production (Py2 floored to 0/1).
    return correct_forecasts / total_forecasts
