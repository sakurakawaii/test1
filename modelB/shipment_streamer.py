"""
shipment_streamer.py

Generator-based readers for the shipment and SKU record streams
consumed by inventory_core.py.
"""

import csv


def _open_source(path):
    # PY3-MIGRATED: In Python 3 csv.reader requires a text-mode file; passing a
    # binary ('rb') handle raises "iterator should return strings, not bytes".
    # Open in text mode with newline='' (the csv module manages line endings).
    # PY3-REVIEW: Field values now decode to str (Python 2 returned bytes). This
    # type flows through the whole pipeline and into the pickled output. Confirm
    # the source encoding is UTF-8; pass encoding=... explicitly if it is not.
    # PY3-REVIEW: File handle is not explicitly closed (matches Python 2 behavior);
    # it is released when the generator is exhausted or garbage-collected. Consider
    # refactoring callers to a `with` block if deterministic close is required.
    return csv.reader(open(path, 'r', newline=''))  # PY3-MIGRATED: 'rb' -> text mode with newline=''


def stream_shipments(path):
    source_iterator = iter(_open_source(path))
    # PY3-MIGRATED: iterator.next() -> next(iterator); guard empty source so a
    # StopIteration is not raised inside the generator (PEP 479 -> RuntimeError).
    try:
        header = next(source_iterator)
    except StopIteration:
        return
    # PY3-MIGRATED: replaced `while True: row = source_iterator.next()` with a
    # for-loop. Under PEP 479 (Python 3.7+) a StopIteration raised inside a
    # generator becomes RuntimeError, so the original exhaustion pattern would crash.
    for row in source_iterator:
        yield dict(zip(header, row))


def stream_filtered_skus(path, sku_prefix):
    for record in stream_shipments(path):
        if record.get('sku', '').startswith(sku_prefix):
            yield record


def stream_with_index(path):
    source_iterator = iter(_open_source(path))
    try:  # PY3-MIGRATED: guard empty source (PEP 479)
        header = next(source_iterator)  # PY3-MIGRATED: .next() -> next()
    except StopIteration:
        return
    # PY3-MIGRATED: for/enumerate replaces `while True: .next()` (PEP 479 safe)
    for index, row in enumerate(source_iterator):
        yield index, dict(zip(header, row))


def stream_chunked_by_warehouse(path, chunk_size):
    source_iterator = iter(_open_source(path))
    try:  # PY3-MIGRATED: guard empty source (PEP 479)
        header = next(source_iterator)  # PY3-MIGRATED: .next() -> next()
    except StopIteration:
        return
    chunk = []
    # PY3-MIGRATED: for-loop replaces `while True: .next()` (PEP 479 safe)
    for row in source_iterator:
        chunk.append(dict(zip(header, row)))
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    # PY3-REVIEW: A trailing partial chunk (< chunk_size) is not yielded. This
    # preserves the original Python 2 behavior, which silently dropped the final
    # partial chunk. Confirm this is intended; if not, add `if chunk: yield chunk`.
