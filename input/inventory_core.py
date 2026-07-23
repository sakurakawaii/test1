#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
inventory_core.py

Primary ETL entry point for the nightly inventory reconciliation
pipeline. Reads inbound shipment and stock-adjustment records, routes
them to the correct warehouse partition, validates and classifies
them, computes rollup metrics, and writes the reconciled output for
downstream systems.

This is the module invoked by run_pipeline.sh. Do not confuse with
inventory_core_v2.py, which is an in-progress rewrite of the routing
layer that is not yet wired into the runner.
"""

import sys
import cPickle as pickle
import ConfigParser
import json

import stock_router
import sku_classifier
import warehouse_session
import warehouse_config
from inventory_metrics import (
    count_stockout_events,
    compute_fill_rate_ratio,
)
from shipment_streamer import stream_shipments


def load_config(path):
    parser = ConfigParser.ConfigParser()
    parser.read(path)
    return parser


def partition_batch(records, partition_count):
    """
    Split incoming records into partition_count buckets using
    stock_router's stable-hash routing.
    """
    buckets = {}
    for record in records:
        bucket = stock_router.route_to_partition(record['sku'], partition_count)
        if not buckets.has_key(bucket):
            buckets[bucket] = []
        buckets[bucket].append(record)
    return buckets


def average_batch_size(total_records, partition_count):
    # Feeds the nightly ops-log summary alongside stockout_ratio and
    # fill_rate below.
    return total_records / partition_count


def reconcile_shipment(record):
    route = sku_classifier.get_route(record)
    record['route'] = route

    try:
        record['unit_cost'] = float(record['unit_cost'])
    except ValueError, e:
        print >> sys.stderr, "Bad unit_cost for sku %s: %s" % (record.get('sku'), e)
        record['unit_cost'] = None

    return record


def run(config_path, input_path, output_path):
    config = load_config(config_path)
    partition_count = config.getint('routing', 'partition_count')

    session = warehouse_session.WarehouseSession(
        operator_id=config.get('auth', 'operator_id'),
        token=warehouse_session.generate_session_token(config.get('auth', 'signing_key')),
        ttl_seconds=config.getint('auth', 'session_ttl_seconds'),
    )

    if not session:
        raise Exception, "Cannot run reconciliation without an authenticated warehouse session"

    records = list(stream_shipments(input_path))
    buckets = partition_batch(records, partition_count)

    reconciled = []
    for bucket_id, bucket_records in buckets.iteritems():
        print "Processing partition %d with %d records" % (bucket_id, len(bucket_records))
        for record in bucket_records:
            reconciled.append(reconcile_shipment(record))

    stockouts = sum(1 for r in reconciled if r.get('on_hand', 0) <= 0)
    stockout_ratio = count_stockout_events(stockouts, len(reconciled) or 1)

    shipped = sum(r.get('units_shipped', 0) for r in reconciled)
    ordered = sum(r.get('units_ordered', 0) for r in reconciled)
    fill_rate = compute_fill_rate_ratio(shipped, ordered or 1)

    summary = {
        'stockout_ratio': stockout_ratio,
        'fill_rate': fill_rate,
        'avg_batch_size': average_batch_size(len(reconciled), partition_count),
        'session_timeout_default': warehouse_config.DEFAULT_TIMEOUT,
    }

    with open(output_path, 'wb') as out:
        pickle.dump({'records': reconciled, 'summary': summary}, out)

    print "Reconciliation complete: %s" % json.dumps(summary)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: inventory_core.py <config> <input> <output>"
        sys.exit(1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
