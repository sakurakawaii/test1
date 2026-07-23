"""
shipment_streamer.py

Generator-based readers for the shipment and SKU record streams
consumed by inventory_core.py.
"""

import csv


def _open_source(path):
    return csv.reader(open(path, 'rb'))


def stream_shipments(path):
    source_iterator = iter(_open_source(path))
    header = source_iterator.next()
    while True:
        row = source_iterator.next()
        yield dict(zip(header, row))


def stream_filtered_skus(path, sku_prefix):
    for record in stream_shipments(path):
        if record.get('sku', '').startswith(sku_prefix):
            yield record


def stream_with_index(path):
    source_iterator = iter(_open_source(path))
    header = source_iterator.next()
    index = 0
    while True:
        row = source_iterator.next()
        yield index, dict(zip(header, row))
        index += 1


def stream_chunked_by_warehouse(path, chunk_size):
    source_iterator = iter(_open_source(path))
    header = source_iterator.next()
    chunk = []
    while True:
        row = source_iterator.next()
        chunk.append(dict(zip(header, row)))
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
