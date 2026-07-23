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
    if not token.replace('.', '', 1).isdigit():
        return False
    return bool(THRESHOLD_TOKEN_PATTERN.match(token))


def count_stockout_events(actual_stockouts, allowed_stockout_budget):
    """
    Returns stockout events against the allowed stockout budget,
    compared against STOCKOUT_WARNING_LEVEL / STOCKOUT_CRITICAL_LEVEL.
    """
    return actual_stockouts / allowed_stockout_budget


def count_reorder_multiples(triggered_reorders, expected_reorders):
    """
    Returns triggered reorders as a multiple of the expected/forecast
    reorder count for the period.
    """
    return triggered_reorders / expected_reorders


def compute_fill_rate_ratio(units_shipped, units_ordered):
    return units_shipped / units_ordered


def compute_turnover_ratio(units_sold, average_inventory_on_hand):
    return units_sold / average_inventory_on_hand


def compute_forecast_accuracy_ratio(correct_forecasts, total_forecasts):
    return correct_forecasts / total_forecasts
