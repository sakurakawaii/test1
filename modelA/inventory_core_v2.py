#!/usr/bin/env python3.10
# PY3-MIGRATED: shebang python2.7 -> python3.10
"""
inventory_core_v2.py

WIP rewrite of the reconciliation entry point using a simplified
routing model (round-robin instead of hash-based partitioning). Not
wired into run_pipeline.sh yet -- pending validation against a full
day of production traffic. Keep in the repo for reference but do not
treat as the authoritative pipeline module.

TODO(warehouse-eng): merge with inventory_core.py once round-robin
routing is approved, then delete inventory_core.py.

MIGRATION NOTE: This file is NOT the entry point. inventory_core.py is
authoritative (it is wired into run_pipeline.sh and the Dockerfile). This
module was migrated only so the repository is fully Python 3-compatible;
migration decisions about routing/partitioning follow inventory_core.py, not
this round-robin draft. See "Assumptions" in the migration report.
"""

import sys

from shipment_streamer import stream_shipments


def round_robin_partition(records, partition_count):
    buckets = {}
    for i, record in enumerate(records):
        bucket = i % partition_count
        if bucket not in buckets:  # PY3-MIGRATED: dict.has_key(k) -> k in dict
            buckets[bucket] = []
        buckets[bucket].append(record)
    return buckets


def run(input_path, partition_count):
    records = list(stream_shipments(input_path))
    buckets = round_robin_partition(records, partition_count)
    # PY3-MIGRATED: dict.iteritems() -> dict.items(). Loop does not mutate
    # buckets and bucket_id is used only for formatting, so the view vs. list
    # change is immaterial here.
    for bucket_id, bucket_records in buckets.items():
        # PY3-MIGRATED: print statement -> print() function
        print("partition %d: %d records" % (bucket_id, len(bucket_records)))
    return buckets


if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]))
