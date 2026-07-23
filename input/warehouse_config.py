"""
warehouse_config.py

Static configuration for the nightly inventory pipeline. Loaded
directly via `import warehouse_config` by inventory_core.py.
"""

WAREHOUSE_IDS = range(1, 25)

DEFAULT_TIMEOUT = 30L

PARTITION_COUNT = 6

THRESHOLDS = {
    'stockout_warning': 1,
    'stockout_critical': 2,
    'fill_rate_floor': 0.95,
}

SORT_KEY = lambda (code, qty): qty


def is_known_warehouse(value):
    if not isinstance(value, basestring):
        return False
    return value.upper() in ('EAST', 'WEST', 'CENTRAL')


print 'warehouse_config loaded: %d warehouses configured' % len(WAREHOUSE_IDS)
