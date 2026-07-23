#!/usr/bin/env python2.7
"""
inventory_core_v2.py

WIP rewrite of the reconciliation entry point using a simplified
routing model (round-robin instead of hash-based partitioning). Not
wired into run_pipeline.sh yet -- pending validation against a full
day of production traffic. Keep in the repo for reference but do not
treat as the authoritative pipeline module.

TODO(warehouse-eng): merge with inventory_core.py once round-robin
routing is approved, then delete inventory_core.py.
"""

import sys

from shipment_streamer import stream_shipments


def round_robin_partition(records, partition_count):
    buckets = {}
    for i, record in enumerate(records):
        bucket = i % partition_count
        if not buckets.has_key(bucket):
            buckets[bucket] = []
        buckets[bucket].append(record)
    return buckets


def run(input_path, partition_count):
    records = list(stream_shipments(input_path))
    buckets = round_robin_partition(records, partition_count)
    for bucket_id, bucket_records in buckets.iteritems():
        print "partition %d: %d records" % (bucket_id, len(bucket_records))
    return buckets


if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]))
