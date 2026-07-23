"""
warehouse_config.py

Static configuration for the nightly inventory pipeline. Loaded
directly via `import warehouse_config` by inventory_core.py.
"""

# PY3-MIGRATED: range() returns a lazy range object in Python 3, not a list.
# Wrapped in list() to preserve the Python 2 list semantics any consumer may
# rely on (indexing, slicing, concatenation, repeated iteration, len()).
WAREHOUSE_IDS = list(range(1, 25))  # PY3-MIGRATED: range() -> list(range()) to keep list type

# PY3-MIGRATED: the Python 2 long literal suffix `L` is a SyntaxError in Python 3.
# Python 3 ints are unbounded, so 30 is an exact equivalent.
DEFAULT_TIMEOUT = 30  # PY3-MIGRATED: 30L -> 30 (no long type in Python 3)

PARTITION_COUNT = 6

THRESHOLDS = {
    'stockout_warning': 1,
    'stockout_critical': 2,
    'fill_rate_floor': 0.95,
}

# PY3-MIGRATED: tuple-unpacking in function/lambda parameters was removed in
# Python 3 (PEP 3113); `lambda (code, qty): qty` is a SyntaxError. Rewritten to
# take a single (code, qty) tuple and index it. Callers using this as a sort key
# over (code, qty) pairs are unaffected.
SORT_KEY = lambda item: item[1]  # PY3-MIGRATED: lambda (code, qty): qty -> lambda item: item[1]


def is_known_warehouse(value):
    # PY3-MIGRATED: `basestring` was removed in Python 3; all text is `str`.
    # Note: Python 2 `basestring` also matched `unicode`; in Python 3 `str` covers
    # both, so behavior is preserved for text inputs.
    if not isinstance(value, str):  # PY3-MIGRATED: basestring -> str
        return False
    return value.upper() in ('EAST', 'WEST', 'CENTRAL')


# PY3-MIGRATED: print statement -> print() function. This runs as an import-time
# side effect (preserved from the original). See report review note.
print('warehouse_config loaded: %d warehouses configured' % len(WAREHOUSE_IDS))  # PY3-MIGRATED: print statement -> print()
