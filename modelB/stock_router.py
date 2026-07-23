"""
stock_router.py

Routes inbound shipment and adjustment records to warehouse processing
partitions.
"""

import hashlib  # PY3-MIGRATED: needed for process-stable hashing (see route_to_partition)


def _stable_partition_hash(value):
    # PY3-MIGRATED: Python 3 salts the builtin hash() of str/bytes per process
    # (PYTHONHASHSEED), so hash(str(sku)) is NOT stable across runs/processes.
    # The original module documents "deterministic"/"stable-hash" routing, so we
    # replace the builtin hash with a content hash that is stable across
    # processes AND Python versions. md5 is used only for bucketing, not security.
    digest = hashlib.md5(str(value).encode('utf-8')).hexdigest()
    return int(digest, 16)


def route_to_partition(sku, partition_count):
    """
    Deterministically assigns a SKU to one of partition_count buckets.
    """
    # PY3-REVIEW: Partition assignment for a given SKU differs from the Python 2
    # builtin-hash result. Within inventory_core.py the final reconciled output is
    # independent of bucket identity (all buckets are reconciled together), but any
    # downstream system that persisted or sharded on the Python 2 partition numbers
    # will see records move. Confirm no such consumer exists before production.
    # --- Original Python 2 line (non-deterministic under Python 3, preserved for audit) ---
    # return hash(str(sku)) % partition_count
    return _stable_partition_hash(sku) % partition_count  # PY3-MIGRATED: process-stable hash replaces salted builtin hash()


def route_batch(records, partition_count):
    routed = {}
    for record in records:
        bucket = route_to_partition(record['sku'], partition_count)
        routed.setdefault(bucket, []).append(record)
    return routed
