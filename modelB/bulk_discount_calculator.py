"""
bulk_discount_calculator.py

Computes volume discounts owed to preferred suppliers based on tiered
rebate rates. Rounding behaviour here has been verified against the
finance team's ledger and is stable across Python versions -- do not
change the rounding approach without sign-off from Finance.
"""

# PY3-REVIEW: The docstring's claim that rounding is "stable across Python
# versions" is INCORRECT for the built-in round(). Python 2 rounds halves away
# from zero (round(10.5) == 11); Python 3 uses banker's rounding / round-half-to-
# even (round(10.5) == 10). With the tier rates below this produces off-by-one-
# dollar rebate drift, e.g. units=105 (10.5 -> was 11, now 10) and
# units=1005 (502.5 -> was 503, now 502). See report item MR (CRITICAL).
# Because this module requires Finance sign-off, the computation line is NOT
# changed unilaterally. The Python 2-equivalent implementation is provided below,
# ready to enable once Finance approves:
#
#     from decimal import Decimal, ROUND_HALF_UP
#     def _compute_tier_rebate(units):
#         rate = _tier_rate_for_units(units)
#         raw_rebate = Decimal(str(units)) * Decimal(str(rate))
#         return int(raw_rebate.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
#
# Decimal also removes the binary float error in `units * rate` (0.1 is inexact),
# which is a second, independent reason to prefer it for monetary math.

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
    # PY3-REVIEW: round() half-rounding differs between Python 2 and 3 (see top of
    # file). Left unchanged pending Finance sign-off; value may drift by $1.
    return round(raw_rebate)


def compute_supplier_rebate(units):
    """
    Returns the whole-dollar rebate owed to a supplier for a shipment
    of `units` items at the applicable tier rate.
    """
    return _compute_tier_rebate(units)
