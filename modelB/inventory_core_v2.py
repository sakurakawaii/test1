#!/usr/bin/env python3
# PY3-MIGRATED: shebang changed from `#!/usr/bin/env python2.7` to python3.
"""
inventory_core_v2.py

WIP rewrite of the reconciliation entry point using a simplified
routing model (round-robin instead of hash-based partitioning). Not
wired into run_pipeline.sh yet -- pending validation against a full
day of production traffic. Keep in the repo for reference but do not
treat as the authoritative pipeline module.

TODO(warehouse-eng): merge with inventory_core.py once round-robin
routing is approved, then delete inventory_core.py.

MIGRATION NOTE: inventory_core.py (not this file) is the authoritative
entry point invoked by run_pipeline.sh. This v2 module was migrated for
completeness but must not be wired in without the team's round-robin
validation. See report Assumptions for the version-conflict record.
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
    # PY3-MIGRATED: dict.iteritems() -> dict.items(); dict not mutated in loop.
    for bucket_id, bucket_records in buckets.items():
        # PY3-MIGRATED: print statement -> print() function
        print("partition %d: %d records" % (bucket_id, len(bucket_records)))
    return buckets


if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]))
