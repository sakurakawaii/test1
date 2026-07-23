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
    # PY3-REVIEW [CRITICAL - silent financial drift; Finance sign-off required]
    # round() changed between Python 2 and 3 in TWO ways that both affect the
    # ledger and neither raises an exception:
    #   1. Rounding mode: Py2 rounds half AWAY FROM ZERO (round(2.5) -> 3.0),
    #      Py3 uses banker's rounding / half-to-even (round(2.5) -> 2).
    #   2. Return type: Py2 round() returns float, Py3 returns int (no ndigits).
    # The module docstring forbids changing the rounding approach without
    # Finance sign-off, so the call is intentionally LEFT AS-IS rather than
    # silently "corrected". If the ledger must match Python 2 exactly, Finance
    # should approve an explicit half-up implementation, e.g.:
    #   from decimal import Decimal, ROUND_HALF_UP
    #   return int(Decimal(raw_rebate).quantize(Decimal('1'), ROUND_HALF_UP))
    # See migration report MR item before promoting to production.
    return round(raw_rebate)


def compute_supplier_rebate(units):
    """
    Returns the whole-dollar rebate owed to a supplier for a shipment
    of `units` items at the applicable tier rate.
    """
    # PY3-REVIEW [CRITICAL - interface/return type]: see _compute_tier_rebate.
    # Return type is now `int` (Py2 returned `float`). Callers not present in
    # this submission that format the result as a float (e.g. "%.2f") or feed
    # it into further float arithmetic must be checked.
    return _compute_tier_rebate(units)
