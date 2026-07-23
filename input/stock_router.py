"""
stock_router.py

Routes inbound shipment and adjustment records to warehouse processing
partitions.
"""


def route_to_partition(sku, partition_count):
    """
    Deterministically assigns a SKU to one of partition_count buckets.
    """
    return hash(str(sku)) % partition_count


def route_batch(records, partition_count):
    routed = {}
    for record in records:
        bucket = route_to_partition(record['sku'], partition_count)
        routed.setdefault(bucket, []).append(record)
    return routed
