"""
warehouse_config.py

Static configuration for the nightly inventory pipeline. Loaded
directly via `import warehouse_config` by inventory_core.py.

MIGRATION NOTE (classification = CONFIGURATION FILE, Python-based):
This file is Python-based config but is imported AS A MODULE and also
exposes executable members (the SORT_KEY callable and the is_known_warehouse
function). Converting it to INI/TOML would break `import warehouse_config`
and drop those callables, so it is intentionally kept as a .py module.
Only Python 2 -> 3 syntax/semantics were changed; values are unchanged.
"""

# PY3-MIGRATED: In Python 2, range() returned a concrete list; Python 3
# returns a lazy range object. Wrapped in list() to preserve the original
# type so any consumer that slices, indexes, mutates, or JSON-serializes
# WAREHOUSE_IDS still behaves as before.
# PY3-REVIEW: if consumers only ever iterate or call len(), the bare range()
# is more memory-efficient and could be used instead.
WAREHOUSE_IDS = list(range(1, 25))

# PY3-MIGRATED: the Python 2 'L' long-integer suffix is a SyntaxError in
# Python 3 (int is unbounded now). Value 30 is unchanged.
DEFAULT_TIMEOUT = 30

PARTITION_COUNT = 6

THRESHOLDS = {
    'stockout_warning': 1,
    'stockout_critical': 2,
    'fill_rate_floor': 0.95,
}

# PY3-MIGRATED: tuple parameter unpacking in lambda/def was removed in
# Python 3 (PEP 3113); `lambda (code, qty): qty` is a SyntaxError. Rewritten
# to index the tuple argument, which returns the identical value for a
# (code, qty) pair used as a sort key.
# PY3-REVIEW: callers (not in this submission) must still pass a 2-tuple/
# sequence; a non-subscriptable argument now raises TypeError at call time
# instead of unpacking at the signature.
SORT_KEY = lambda item: item[1]


def is_known_warehouse(value):
    # PY3-MIGRATED: basestring was removed in Python 3; replaced with str.
    # PY3-REVIEW [str/bytes]: in Python 2 basestring also matched byte
    # strings. If any caller passes bytes (e.g. b'EAST'), this now returns
    # False where Python 2 returned True. Warehouse codes are expected to be
    # text (str); confirm no caller passes bytes.
    if not isinstance(value, str):
        return False
    return value.upper() in ('EAST', 'WEST', 'CENTRAL')


# PY3-MIGRATED: print statement -> print() function.
# PY3-REVIEW: this is an IMPORT-TIME side effect (it runs every time the
# module is imported, including by inventory_core.py) and writes to stdout.
# Behaviour preserved, but consider moving to the logging module so it does
# not pollute pipeline stdout / the reconciliation summary output.
print('warehouse_config loaded: %d warehouses configured' % len(WAREHOUSE_IDS))
