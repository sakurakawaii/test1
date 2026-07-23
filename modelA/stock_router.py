"""
stock_router.py

Routes inbound shipment and adjustment records to warehouse processing
partitions.
"""


def route_to_partition(sku, partition_count):
    """
    Deterministically assigns a SKU to one of partition_count buckets.
    """
    # PY3-REVIEW [HIGH - routing stability]: Python 3 applies hash
    # randomization to str objects by default (PEP 456 / PYTHONHASHSEED), so
    # `hash(str(sku))` is NO LONGER stable across interpreter processes. The
    # same SKU can land in a different partition on each nightly run, breaking
    # the "stable-hash routing" this module documents. Behaviour is NOT
    # preserved and cannot be preserved by a drop-in edit, so the line is left
    # runnable but flagged for a decision:
    #   (a) pin PYTHONHASHSEED=0 in run_pipeline.sh / Dockerfile (restores
    #       per-deployment determinism, but values still differ from Py2), or
    #   (b) replace with a content hash that is stable everywhere, e.g.:
    #         import hashlib
    #         digest = hashlib.md5(str(sku).encode('utf-8')).hexdigest()
    #         return int(digest, 16) % partition_count
    #       (this changes the partition distribution vs. Python 2 and must be
    #        validated against downstream partition consumers before rollout).
    return hash(str(sku)) % partition_count


def route_batch(records, partition_count):
    routed = {}
    for record in records:
        bucket = route_to_partition(record['sku'], partition_count)
        routed.setdefault(bucket, []).append(record)
    return routed
