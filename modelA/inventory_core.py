#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# PY3-MIGRATED: shebang python2.7 -> python3.10 (see run_pipeline.sh note).
# NOTE: the coding declaration above is kept on line 2 so Python still honors
# it; it is redundant in Python 3 (UTF-8 is the default source encoding).
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
import configparser  # PY3-MIGRATED: ConfigParser -> configparser (module rename)
import json

# PY3-REVIEW [MEDIUM - implicit relative imports]: these are flat/absolute
# imports of sibling modules. They resolve only because run_pipeline.sh puts
# the module directory on PYTHONPATH and the script's own directory is on
# sys.path[0]. They are NOT package-relative; if this code is ever packaged
# (added to a package with __init__.py), change to `from . import ...`.
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
    # PY3-MIGRATED + PY3-REVIEW [CRITICAL - integer division]: `/` was floor
    # division in Python 2 (both args are int record/partition counts) and is
    # true division in Python 3. This is a batch-count calculation, so per
    # migration policy it is converted to `//` to PRESERVE the exact Python 2
    # integer result that the ops-log summary currently reports.
    # ACTION: confirm with ops whether avg_batch_size should remain an integer
    # (keep //) or become a fractional average (change to /). Value feeds
    # summary['avg_batch_size'] and is JSON-serialized downstream.
    return total_records // partition_count


def reconcile_shipment(record):
    route = sku_classifier.get_route(record)
    record['route'] = route

    try:
        record['unit_cost'] = float(record['unit_cost'])
    except ValueError as e:  # PY3-MIGRATED: `except ValueError, e:` -> `as e`
        # PY3-MIGRATED: `print >> sys.stderr, msg` -> print(msg, file=sys.stderr)
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

    # PY3-REVIEW [CRITICAL - cross-module]: this truthiness check depends on
    # WarehouseSession.__bool__ (renamed from __nonzero__ during migration).
    # If that rename is ever reverted, Python 3 ignores __nonzero__ and every
    # session becomes truthy, SILENTLY disabling this auth gate. Verified
    # consistent with warehouse_session.py in this submission.
    if not session:
        raise Exception("Cannot run reconciliation without an authenticated warehouse session")  # PY3-MIGRATED: `raise Exception, "msg"` -> `raise Exception("msg")`

    records = list(stream_shipments(input_path))
    buckets = partition_batch(records, partition_count)

    reconciled = []
    # PY3-MIGRATED: dict.iteritems() -> dict.items(). Safe here: the loop does
    # not mutate `buckets`, and bucket_id is used only for formatting, not
    # positional indexing, so the view vs. list change has no effect.
    for bucket_id, bucket_records in buckets.items():
        # PY3-MIGRATED: print statement -> print() function
        print("Processing partition %d with %d records" % (bucket_id, len(bucket_records)))
        for record in bucket_records:
            reconciled.append(reconcile_shipment(record))

    # PY3-REVIEW [HIGH - str/int comparison at CSV boundary]: records come
    # from shipment_streamer, where every value is a str (CSV text). If any
    # record has an 'on_hand' key, `'5' <= 0` raises TypeError in Python 3
    # ('<=' not supported between str and int); Python 2 silently returned
    # False. If 'on_hand' is always absent, the default 0 makes `0 <= 0` True
    # and every record counts as a stockout. ACTION: coerce on_hand to a
    # number explicitly in reconcile_shipment (e.g. int(record.get('on_hand',
    # 0) or 0)), or confirm the field is never present. Line left unchanged to
    # avoid silently altering current numeric behaviour.
    stockouts = sum(1 for r in reconciled if r.get('on_hand', 0) <= 0)
    # PY3-REVIEW [CRITICAL - silent numeric drift]: count_stockout_events uses
    # `/`, which was floor division in Python 2 (inventory_metrics.py has no
    # __future__ division) and is true division in Python 3. stockout_ratio
    # output changes (e.g. 3 stockouts / 100 records was 0 in Py2, is 0.03
    # now). See inventory_metrics.py.
    stockout_ratio = count_stockout_events(stockouts, len(reconciled) or 1)

    # PY3-REVIEW [HIGH - str/int sum at CSV boundary]: units_shipped /
    # units_ordered are str values from the CSV when present. `sum(..)` with a
    # str element raises TypeError in BOTH Python 2 and 3 (0 + '5'); this only
    # "works" today if those columns are absent (sum == 0). ACTION: coerce to
    # int/float before summing, or confirm the columns are never present.
    shipped = sum(r.get('units_shipped', 0) for r in reconciled)
    ordered = sum(r.get('units_ordered', 0) for r in reconciled)
    # PY3-REVIEW [CRITICAL - silent numeric drift]: compute_fill_rate_ratio
    # uses `/`; floor division in Python 2, true division in Python 3. Compared
    # downstream against FILL_RATE_FLOOR (0.95), so true division is the
    # intended behaviour, but fill_rate values change vs. production.
    fill_rate = compute_fill_rate_ratio(shipped, ordered or 1)

    summary = {
        'stockout_ratio': stockout_ratio,
        'fill_rate': fill_rate,
        'avg_batch_size': average_batch_size(len(reconciled), partition_count),
        'session_timeout_default': warehouse_config.DEFAULT_TIMEOUT,
    }

    # PY3-REVIEW [CRITICAL - pickle serialization boundary]: output is written
    # with pickle in binary mode (correct). Two cross-version hazards: (1) a
    # Python 3 pickle cannot be read by any downstream consumer still running
    # Python 2; (2) the reconciled record string values are now Python 3 str
    # (text) rather than Python 2 bytes-str. Confirm every consumer of
    # output_*.pkl runs Python 3. Consider pinning protocol (e.g.
    # pickle.dump(..., protocol=4)) and documenting it for downstream readers.
    with open(output_path, 'wb') as out:
        pickle.dump({'records': reconciled, 'summary': summary}, out)

    # PY3-MIGRATED: print statement -> print() function
    print("Reconciliation complete: %s" % json.dumps(summary))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        # PY3-MIGRATED: `print >> sys.stderr, msg` -> print(msg, file=sys.stderr)
        print("usage: inventory_core.py <config> <input> <output>", file=sys.stderr)
        sys.exit(1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])
