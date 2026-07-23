"""
shipment_streamer.py

Generator-based readers for the shipment and SKU record streams
consumed by inventory_core.py.
"""

import csv


def _open_source(path):
    # PY3-MIGRATED: csv in Python 3 requires a TEXT-mode file; opening 'rb'
    # yields bytes and raises "_csv.Error: iterator should return strings,
    # not bytes". newline='' is the documented csv requirement to avoid
    # double-newline translation.
    # PY3-REVIEW: encoding defaulted to 'utf-8'; confirm the warehouse
    # management system emits UTF-8 (or set the correct encoding/errors).
    # Also note: this file handle is never explicitly closed (pre-existing
    # behaviour, preserved) - consider a context manager in a future change.
    return csv.reader(open(path, 'r', newline='', encoding='utf-8'))


def stream_shipments(path):
    source_iterator = iter(_open_source(path))
    # PY3-MIGRATED: .next() -> next(); and the original `while True: next()`
    # relied on StopIteration escaping the generator to terminate it. Under
    # PEP 479 (Python 3.7+) that StopIteration becomes RuntimeError. Reading
    # the header in a guarded block and iterating the rest with a for-loop
    # preserves the exact semantics (first row = header) while terminating
    # cleanly. See MR items in the migration report.
    try:
        header = next(source_iterator)
    except StopIteration:
        return
    for row in source_iterator:
        yield dict(zip(header, row))


def stream_filtered_skus(path, sku_prefix):
    for record in stream_shipments(path):
        if record.get('sku', '').startswith(sku_prefix):
            yield record


def stream_with_index(path):
    source_iterator = iter(_open_source(path))
    # PY3-MIGRATED: .next() -> next() and PEP 479-safe restructure (see above).
    try:
        header = next(source_iterator)
    except StopIteration:
        return
    index = 0
    for row in source_iterator:
        yield index, dict(zip(header, row))
        index += 1


def stream_chunked_by_warehouse(path, chunk_size):
    source_iterator = iter(_open_source(path))
    # PY3-MIGRATED: .next() -> next() and PEP 479-safe restructure (see above).
    try:
        header = next(source_iterator)
    except StopIteration:
        return
    chunk = []
    for row in source_iterator:
        chunk.append(dict(zip(header, row)))
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    # PY3-REVIEW: a trailing partial chunk (len < chunk_size) is not yielded.
    # This matches the Python 2 behaviour exactly (the original `while True`
    # loop also dropped any final partial chunk), so it is preserved. Confirm
    # with the reporting team whether the final partial chunk should be
    # emitted; if so, add `if chunk: yield chunk` here.
