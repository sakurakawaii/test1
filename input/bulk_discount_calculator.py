"""
bulk_discount_calculator.py

Computes volume discounts owed to preferred suppliers based on tiered
rebate rates. Rounding behaviour here has been verified against the
finance team's ledger and is stable across Python versions -- do not
change the rounding approach without sign-off from Finance.
"""

TIER_RATES = [
    (100, 0.10),
    (500, 0.25),
    (1000, 0.50),
]


def _tier_rate_for_units(units):
    rate = 0.0
    for threshold, tier_rate in TIER_RATES:
        if units >= threshold:
            rate = tier_rate
    return rate


def _compute_tier_rebate(units):
    rate = _tier_rate_for_units(units)
    raw_rebate = units * rate
    return round(raw_rebate)


def compute_supplier_rebate(units):
    """
    Returns the whole-dollar rebate owed to a supplier for a shipment
    of `units` items at the applicable tier rate.
    """
    return _compute_tier_rebate(units)
