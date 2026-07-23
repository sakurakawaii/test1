#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PY3-MIGRATED: shebang changed from `#!/usr/bin/env python2.7` to python3
# (annotation kept off the shebang line itself; a trailing comment there would be
# passed to env as arguments and break execution).
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
import pickle  # PY3-MIGRATED: cPickle -> pickle (cPickle merged into pickle)
import configparser  # PY3-MIGRATED: ConfigParser -> configparser
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
    parser = configparser.ConfigParser()  # PY3-MIGRATED: ConfigParser.ConfigParser -> configparser.ConfigParser
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
        if bucket not in buckets:  # PY3-MIGRATED: dict.has_key(k) -> k in dict
            buckets[bucket] = []
        buckets[bucket].append(record)
    return buckets


def average_batch_size(total_records, partition_count):
    # Feeds the nightly ops-log summary alongside stockout_ratio and
    # fill_rate below.
    # PY3-REVIEW: CRITICAL - Python 2 `/` on two ints floored to an int; Python 3
    # `/` is true division (float). This is a batch COUNT, so floor division (//)
    # is used to preserve the Python 2 integer result and keep the summary field
    # an int. If a fractional average is actually wanted, change back to `/` and
    # confirm downstream consumers of 'avg_batch_size' accept a float. (report MR)
    # --- Original Python 2 line (int floor division) ---
    # return total_records / partition_count
    return total_records // partition_count  # PY3-MIGRATED: `/` -> `//` to preserve Py2 integer batch size


def reconcile_shipment(record):
    route = sku_classifier.get_route(record)
    record['route'] = route

    try:
        record['unit_cost'] = float(record['unit_cost'])
    except ValueError as e:  # PY3-MIGRATED: `except ValueError, e:` -> `except ValueError as e:`
        # PY3-MIGRATED: print >> sys.stderr, ... -> print(..., file=sys.stderr)
        print("Bad unit_cost for sku %s: %s" % (record.get('sku'), e), file=sys.stderr)
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

    # PY3-REVIEW: This guard depends on WarehouseSession.__bool__ (was __nonzero__
    # in Python 2). The rename is applied in warehouse_session.py; if it is ever
    # reverted, this check silently becomes always-False and the pipeline runs
    # without an authenticated session. (report cross-module warning)
    if not session:
        raise Exception("Cannot run reconciliation without an authenticated warehouse session")  # PY3-MIGRATED: `raise Exception, "msg"` -> `raise Exception("msg")`

    records = list(stream_shipments(input_path))
    buckets = partition_batch(records, partition_count)

    reconciled = []
    # PY3-MIGRATED: dict.iteritems() -> dict.items(). The dict is not mutated
    # during iteration, so the view vs list difference is safe here.
    for bucket_id, bucket_records in buckets.items():
        # PY3-MIGRATED: print statement -> print() function
        print("Processing partition %d with %d records" % (bucket_id, len(bucket_records)))
        for record in bucket_records:
            reconciled.append(reconcile_shipment(record))

    stockouts = sum(1 for r in reconciled if r.get('on_hand', 0) <= 0)
    # PY3-REVIEW: r.get('on_hand', 0) compares a CSV string to 0 when the key is
    # present; shipment_streamer now yields str values. '5' <= 0 raises TypeError
    # in Python 3 (Python 2 compared by type name and silently returned False).
    # Confirm 'on_hand' is absent in the feed (default 0) or coerce to int first.
    stockout_ratio = count_stockout_events(stockouts, len(reconciled) or 1)

    shipped = sum(r.get('units_shipped', 0) for r in reconciled)
    ordered = sum(r.get('units_ordered', 0) for r in reconciled)
    # PY3-REVIEW: same str/int concern - if 'units_shipped'/'units_ordered' are
    # present they are str (from CSV); sum() starting at int 0 raises TypeError in
    # both Python 2 and 3. Coerce to numeric in reconcile_shipment if these fields
    # are populated. fill_rate return type is now float (see inventory_metrics).
    fill_rate = compute_fill_rate_ratio(shipped, ordered or 1)

    summary = {
        'stockout_ratio': stockout_ratio,
        'fill_rate': fill_rate,
        'avg_batch_size': average_batch_size(len(reconciled), partition_count),
        'session_timeout_default': warehouse_config.DEFAULT_TIMEOUT,
    }

    # PY3-REVIEW: CRITICAL - output is written with the default pickle protocol,
    # which in Python 3 is protocol >=3 and is NOT readable by any Python 2
    # consumer of this .pkl. Record values are now str (were bytes) and
    # stockout_ratio/fill_rate are now float. If a Python 2 reader still exists
    # downstream, pass protocol=2 AND confirm the str/float type changes are
    # acceptable. (report MR)
    with open(output_path, 'wb') as out:
        pickle.dump({'records': reconciled, 'summary': summary}, out)

    # PY3-MIGRATED: print statement -> print() function
    print("Reconciliation complete: %s" % json.dumps(summary))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        # PY3-MIGRATED: print >> sys.stderr, ... -> print(..., file=sys.stderr)
        print("usage: inventory_core.py <config> <input> <output>", file=sys.stderr)
        sys.exit(1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
