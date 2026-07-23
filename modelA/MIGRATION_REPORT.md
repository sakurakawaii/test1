# Migration Report

**Submission Date:** 2026-07-18 | **Overall Risk:** CRITICAL
**Files Processed:** 25 (15 Python source, 1 INI config, 2 dependency manifests, 2 runner/env, 1 opaque `.pyc`, 4 frontend assets) | **Changes Applied:** 45 | **Review Flags:** 35

> **Target:** Python 2.7 → Python 3.10. Validation was performed on Python 3.12 in the sandbox (syntax + runtime smoke test); all findings below were verified empirically. Re-validate on a true 3.10 interpreter before production.
>
> **Why CRITICAL overall:** three independent *silent* data-corruption vectors are present — (a) integer/true-division drift in aggregation and alert metrics (`inventory_metrics.py`, `inventory_core.py`), (b) `round()` rounding-mode change in a Finance-owned rebate calculation (`bulk_discount_calculator.py`), and (c) str/bytes changes across the `pickle` serialization boundary (`inventory_core.py`). In addition, one shipped artifact (`legacy_price_lookup.pyc`) has no recoverable source.

---

## Module Dependency Graph & Execution Order

**Entry point:** `inventory_core.py` (invoked by `run_pipeline.sh` and the `Dockerfile` `CMD`).

```
run_pipeline.sh / Dockerfile
        └── inventory_core.py  (PIPELINE, entry point)
              ├── shipment_streamer.py   (UTILITY)
              ├── stock_router.py        (UTILITY)
              ├── sku_classifier.py      (UTILITY)
              ├── warehouse_session.py   (UTILITY)
              ├── warehouse_config.py    (CONFIG, Python-based, imported as a module)
              └── inventory_metrics.py   (UTILITY: count_stockout_events, compute_fill_rate_ratio)

inventory_core_v2.py  (PIPELINE, WIP alternate entry point — NOT wired in)
              └── shipment_streamer.py

Not imported by the entry point in this submission (standalone UTILITY modules):
  bulk_discount_calculator.py, inventory_reporting_utils.py, purchase_order_validator.py,
  sku_validator.py, stock_analytics.py, store_validator.py, supplier_contact_validator.py
```

Shared utilities were migrated **before** the pipeline modules that consume them, and shared-function return types were checked for consistency across every caller in the submission (see *Cross-Module Interface Warnings*).

---

## inventory_core.py
**Classification:** PIPELINE MODULE (entry point) | **Risk:** CRITICAL | **Changes:** 13 | **Flags:** 8

### Changes Made
- [Line 1] Shebang: `#!/usr/bin/env python2.7` -> `#!/usr/bin/env python3.10`
- [Line 21] Stdlib rename: `import cPickle as pickle` -> `import pickle`
- [Line 22] Stdlib rename: `import ConfigParser` -> `import configparser`
- [Line 42] API: `ConfigParser.ConfigParser()` -> `configparser.ConfigParser()`
- [Line 55] Dict API: `buckets.has_key(bucket)` -> `bucket not in buckets`
- [Line 72] Division: `total_records / partition_count` -> `total_records // partition_count` (see MR-01)
- [Line 81] Exception syntax: `except ValueError, e:` -> `except ValueError as e:`
- [Line 83] Print: `print >> sys.stderr, "..."` -> `print("...", file=sys.stderr)`
- [Line 105] Raise syntax: `raise Exception, "..."` -> `raise Exception("...")`
- [Line 114] Dict API: `buckets.iteritems()` -> `buckets.items()` (non-mutating loop; safe)
- [Line 116] Print: `print "Processing partition..."` -> `print("Processing partition...")`
- [Line 168] Print: `print "Reconciliation complete..."` -> `print("Reconciliation complete...")`
- [Line 174] Print: `print >> sys.stderr, "usage..."` -> `print("usage...", file=sys.stderr)`

### Manual Review Required
- [MR-01 | CRITICAL] Line 72 `average_batch_size`: Python 2 performed floor division here (two integer counts); Python 3 `/` is true division. Converted to `//` to **preserve the exact integer value** currently reported in `summary['avg_batch_size']` (verified: 4 records // 3 partitions = 1). Confirm with ops whether avg batch size must stay an integer (keep `//`) or should become a fractional average (change to `/`). Silent drift risk in the ops-log summary.
- [MR-02 | CRITICAL] Line 135 `stockout_ratio = count_stockout_events(stockouts, len(reconciled) or 1)`: `count_stockout_events` uses `/`, which was **floor** division in Python 2 (`inventory_metrics.py` has no `from __future__ import division`). Example drift: 3 stockouts / 100 records was `0` in Py2, is `0.03` now. The value feeds the nightly stockout alert and is JSON-serialized. Confirm the alert threshold logic expects the fractional ratio.
- [MR-03 | CRITICAL] Line 148 `fill_rate = compute_fill_rate_ratio(shipped, ordered or 1)`: same floor→true division change. `fill_rate` is compared downstream against `FILL_RATE_FLOOR = 0.95`, so true division is the clear design intent and Python 2 was effectively a latent bug (value was always 0 or 1). Output values will change; requires ops/Finance sign-off.
- [MR-04 | CRITICAL] Line 165 `pickle.dump({'records': reconciled, 'summary': summary}, out)`: two serialization-boundary hazards. (1) A Python 3 pickle cannot be read by any downstream consumer still running Python 2. (2) Record string values are now Python 3 `str` (text), not Python 2 bytes-`str`. Action: confirm every consumer of `/data/reconciled/output_*.pkl` runs Python 3; pin an explicit `protocol=` and document it for downstream readers.
- [MR-05 | HIGH] Line 129 `sum(1 for r in reconciled if r.get('on_hand', 0) <= 0)`: records come from `shipment_streamer`, where every field is a `str` (CSV text). **Verified:** if any record carries an `on_hand` key, `'5' <= 0` raises `TypeError: '<=' not supported between instances of 'str' and 'int'` in Python 3 (Python 2 silently returned `False`). If `on_hand` is always absent, the default `0` makes `0 <= 0` True and **every** record is counted as a stockout (smoke test produced `stockout_ratio = 1.0`). Action: coerce `on_hand` to a number in `reconcile_shipment` (e.g. `int(record.get('on_hand', 0) or 0)`), or confirm the column is never present. Line left unchanged to avoid silently altering current numeric behaviour.
- [MR-06 | HIGH] Lines 142–143 `sum(r.get('units_shipped', 0) ...)` / `units_ordered`: same CSV-string issue. `sum()` with a `str` element raises `TypeError` in **both** Python 2 and 3 (`0 + '5'`), so this only "works" today if those columns are absent (sum == 0, producing `fill_rate = 0.0` in the smoke test). Action: coerce to `int`/`float` before summing, or confirm the columns are never present.
- [MR-07 | MEDIUM] Lines 30–37 (`import stock_router`, etc.): these are flat/implicit-relative imports. They resolve only because `run_pipeline.sh` exports `PYTHONPATH=$(pwd)` and the script's directory is on `sys.path[0]`. They are **not** package-relative; if this code is ever packaged (given an `__init__.py`), they break. Left as-is because changing to `from . import ...` would break the current script-style invocation.
- [MR-08 | CRITICAL (cross-module)] Line 104 `if not session:`: depends on `WarehouseSession.__bool__` (renamed from `__nonzero__`, see MR-16). If that rename is reverted, Python 3 ignores `__nonzero__`, every session becomes truthy, and this auth gate is **silently disabled**. Verified consistent within this submission.

---

## inventory_metrics.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 0 code edits (behaviour changes without a visible edit — see below) | **Flags:** 2

> **Most dangerous file in the submission.** No line needed a *syntactic* change, so a mechanical migration tool would report "0 changes" — yet every division's runtime result changes. This module has **no** `from __future__ import division`, so in Python 2 all five `/` operators were **floor** division; in Python 3 they are true division. I deliberately kept `/` (did not convert to `//`) because each result is a ratio compared against a fractional threshold, making true division the clear design intent — but the nightly output values change.

### Changes Made
- None (all `/` operators left as `/`; review annotations added inline).

### Manual Review Required
- [MR-09 | CRITICAL] Floor→true division on lines **45** (`count_stockout_events`), **57** (`count_reorder_multiples`), **67** (`compute_fill_rate_ratio`), **74** (`compute_turnover_ratio`), **81** (`compute_forecast_accuracy_ratio`). The `_ratio` functions are compared against fractional floors (`FILL_RATE_FLOOR=0.95`, `TURNOVER_FLOOR=0.80`, `FORECAST_ACCURACY_FLOOR=0.90`), so true division is correct and Python 2 was a latent bug (always 0 or 1). **Action:** get ops/Finance sign-off that the corrected ratios are desired, and re-baseline any alert thresholds that were tuned against the old floored values. Do **not** "fix" by adding `//` — that would re-introduce the Python 2 bug.
- [MR-10 | MEDIUM] Line 23 `is_valid_threshold_token`: `str.isdigit()` and `\d` match non-ASCII digits in Python 3; if threshold tokens can contain non-ASCII input, this now accepts values Python 2 rejected. Compile with `re.ASCII` / restrict to ASCII if strict behaviour is required.

---

## bulk_discount_calculator.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 0 code edits (intentional — Finance sign-off required) | **Flags:** 1

### Changes Made
- None. `round(raw_rebate)` on line 41 was **intentionally left unchanged**. The module docstring explicitly forbids changing the rounding approach without Finance sign-off, so it is flagged rather than silently altered.

### Manual Review Required
- [MR-11 | CRITICAL] Line 41 `return round(raw_rebate)`: `round()` changed in two silent ways between Python 2 and 3. (1) **Rounding mode:** Python 2 rounds half away from zero (`round(10.5)=11.0`), Python 3 uses banker's rounding / half-to-even (`round(10.5)=10`). (2) **Return type:** Python 2 `round()` returns `float`, Python 3 returns `int`. **Verified drift in context:** 332 of the first 2,000 unit counts produce a different rebate; e.g. 105 units @ 0.10 = `10.5` → **$11 (Py2) vs $10 (Py3)**. This directly affects the Finance ledger with no exception raised. **Action:** Finance must decide whether the ledger must match Python 2 exactly; if so, approve an explicit half-up implementation, e.g. `int(Decimal(repr(raw_rebate)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))`. See also the return-type change under *Cross-Module Interface Warnings*.

---

## shipment_streamer.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 4 | **Flags:** 4

### Changes Made
- [Line 20] str/bytes file I/O: `csv.reader(open(path, 'rb'))` -> `csv.reader(open(path, 'r', newline='', encoding='utf-8'))`
- [Lines 32/49/62] Iterator protocol: `source_iterator.next()` -> `next(source_iterator)` (header reads)
- [Lines 28–37 / 45–54 / 57–68] Control flow (PEP 479): the `while True: row = source_iterator.next()` pattern was restructured to a guarded header read plus a `for row in source_iterator:` loop in all three generators.

### Manual Review Required
- [MR-12 | CRITICAL] Line 20: in Python 3, `csv.reader` over a binary (`'rb'`) handle raises `_csv.Error: iterator should return strings, not bytes`. Opened in text mode with `newline=''` (the documented csv requirement). This is a str/bytes boundary: dict **values** are now `str` (text) rather than Python 2 bytes-`str`, which flows into `reconcile_shipment`, routing, and the pickled output (see MR-04).
- [MR-13 | HIGH] Lines 28–68 (all three generators): the original relied on `StopIteration` escaping the generator to terminate the `while True` loop. Under **PEP 479** (Python 3.7+) that `StopIteration` becomes `RuntimeError: generator raised StopIteration`. Restructured to terminate cleanly. **Verified:** empty and header-only files now yield `[]` instead of raising. Confirm the restructure preserves intended behaviour for your feeds.
- [MR-14 | MEDIUM] Line 20: encoding defaulted to `utf-8`. Confirm the warehouse management system emits UTF-8 (set the correct `encoding`/`errors` otherwise). The file handle is also never explicitly closed (pre-existing; preserved) — consider a context manager.
- [MR-15 | MEDIUM] Line 68 `stream_chunked_by_warehouse`: a trailing partial chunk (`len < chunk_size`) is **not** yielded. This exactly matches the Python 2 behaviour and is preserved, but confirm the reporting team does not expect the final partial chunk; if they do, add `if chunk: yield chunk`.

---

## warehouse_session.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 4 | **Flags:** 3

### Changes Made
- [Line 30] Dunder rename: `def __nonzero__(self):` -> `def __bool__(self):`
- [Line 42] `is_expired`: `return not self.__nonzero__()` -> `return not bool(self)`
- [Line 56] str/bytes: `hashlib.sha256(signing_key + payload)` -> `hashlib.sha256((signing_key + payload).encode('utf-8'))`
- [Line 65] str/bytes: `return str(signature)` -> `return signature.decode('ascii')`

### Manual Review Required
- [MR-16 | CRITICAL] Line 30 `__nonzero__` → `__bool__`: Python 3 **ignores** `__nonzero__`, which would make every `WarehouseSession` truthy and silently bypass the `if not session:` auth gate in `inventory_core.py` (MR-08). Fixed; verified `bool(fresh)=True`, `bool(empty-token)=False`. Interface-critical: any external caller that called `.__nonzero__()` directly must switch to `bool(session)`.
- [MR-17 | CRITICAL] Line 56: `hashlib.sha256` requires `bytes` in Python 3; passing `str` raises `TypeError: Strings must be encoded before hashing`. Encoded as UTF-8. If `signing_key` is ever supplied as raw `bytes` (e.g. from a binary keystore), re-encoding will fail — branch on type if that is possible.
- [MR-18 | CRITICAL] Line 65: `base64.urlsafe_b64encode` returns `bytes` in Python 3; the original `str(signature)` produced the **bytes repr** (e.g. `"b'UU...='"`), silently corrupting the token. `.decode('ascii')` reproduces the Python 2 value. **Verified** the returned token is a clean `str` not beginning with `b'`. The token value is unchanged for an identical `signing_key`, but verify any tokens persisted/compared across systems still match.

---

## stock_router.py
**Classification:** UTILITY / HELPER | **Risk:** HIGH | **Changes:** 0 | **Flags:** 1

### Changes Made
- None (code is syntactically valid Python 3; the behavioural issue cannot be fixed by a drop-in edit — see below).

### Manual Review Required
- [MR-19 | HIGH] Line 28 `return hash(str(sku)) % partition_count`: Python 3 randomizes `str` hashing per process by default (PEP 456 / `PYTHONHASHSEED`), so this is **no longer deterministic** across runs — the same SKU can land in a different partition on each nightly run, breaking the "stable-hash routing" the module documents. Behaviour cannot be preserved by a drop-in edit. **Action (choose one):** (a) export `PYTHONHASHSEED=0` in `run_pipeline.sh`/`Dockerfile` (restores per-deployment determinism; values still differ from the Python 2 era), or (b) switch to a content hash, e.g. `int(hashlib.md5(str(sku).encode('utf-8')).hexdigest(), 16) % partition_count` (stable everywhere but changes the partition distribution vs. Python 2 — validate against downstream partition consumers first). Relevant config: `[routing] hash_seed_pinned = false`.

---

## warehouse_config.py
**Classification:** CONFIGURATION FILE (Python-based) | **Risk:** MEDIUM | **Changes:** 5 | **Flags:** 4

> **Structural decision:** this is Python-based config but is imported *as a module* (`import warehouse_config`) and exposes executable members (`SORT_KEY` callable, `is_known_warehouse` function). Converting it to INI/TOML would break the import and drop those callables, so it is **kept as a `.py` module**. Only Python 2→3 syntax/semantics were changed; all values are unchanged. Two of the original lines (`30L` and the tuple-unpacking lambda) were hard `SyntaxError`s that would have blocked import of the entire pipeline.

### Changes Made
- [Line 21] Sequence type: `WAREHOUSE_IDS = range(1, 25)` -> `WAREHOUSE_IDS = list(range(1, 25))` (preserve list type)
- [Line 25] Long literal removed: `DEFAULT_TIMEOUT = 30L` -> `DEFAULT_TIMEOUT = 30`
- [Line 42] Tuple-param unpacking (PEP 3113): `SORT_KEY = lambda (code, qty): qty` -> `SORT_KEY = lambda item: item[1]`
- [Line 51] `basestring` removed: `isinstance(value, basestring)` -> `isinstance(value, str)`
- [Line 61] Print: `print '...' % ...` -> `print('...' % ...)`

### Manual Review Required
- [MR-20 | MEDIUM] Line 21: Python 2 `range()` returned a list; consumers that index/slice/mutate/JSON-serialize `WAREHOUSE_IDS` rely on that. Wrapped in `list()` to preserve the type for callers not in this submission.
- [MR-21 | MEDIUM] Line 42 `SORT_KEY`: the rewrite returns the identical value for a `(code, qty)` pair, but the call convention changed — a non-subscriptable argument now raises `TypeError` at call time instead of unpacking at the signature. Confirm all callers pass a 2-tuple/sequence.
- [MR-22 | MEDIUM] Line 51 `is_known_warehouse`: Python 2 `basestring` also matched byte strings. If any caller passes `bytes` (e.g. `b'EAST'`), this now returns `False` where Python 2 returned `True`. Warehouse codes are expected to be text.
- [MR-23 | MEDIUM] Line 61: this `print` is an **import-time side effect** (runs every time the module is imported, including by `inventory_core.py`) writing to stdout. Behaviour preserved (smoke test showed `warehouse_config loaded: 24 warehouses configured`), but consider moving to `logging` so it does not pollute pipeline stdout.

---

## inventory_core_v2.py
**Classification:** PIPELINE MODULE (WIP alternate entry point) | **Risk:** MEDIUM | **Changes:** 4 | **Flags:** 1

> **Not treated as interchangeable with `inventory_core.py`.** `inventory_core.py` is authoritative (wired into `run_pipeline.sh` and the `Dockerfile`, and documented as the entry point). This WIP module uses a different routing model (round-robin vs. hash-based). It was migrated only so the repository is fully Python 3-compatible; all partitioning/type decisions follow `inventory_core.py`. See *Assumptions* #2.

### Changes Made
- [Line 1] Shebang: `#!/usr/bin/env python2.7` -> `#!/usr/bin/env python3.10`
- [Line 31] Dict API: `buckets.has_key(bucket)` -> `bucket not in buckets`
- [Line 43] Dict API: `buckets.iteritems()` -> `buckets.items()` (non-mutating loop; safe)
- [Line 45] Print: `print "partition..."` -> `print("partition...")`

### Manual Review Required
- [MR-24 | MEDIUM] This module implements round-robin partitioning, which produces a **different partition assignment** than the authoritative hash-based `inventory_core.py`. Do not swap it into the runner without the validation the docstring's TODO calls for. Note it also consumes the migrated `shipment_streamer` generators (MR-13).

---

## sku_classifier.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 0 | **Flags:** 0

### Changes Made
- None. No Python 2 constructs; uses only `dict.get`. Copied unchanged; interface (`get_route(record) -> str`) preserved.

### Manual Review Required
- None.

---

## sku_validator.py / purchase_order_validator.py / store_validator.py / supplier_contact_validator.py / inventory_reporting_utils.py
**Classification:** UTILITY / HELPER (×5) | **Risk:** LOW | **Changes:** 0 (executable code byte-identical; verified by AST comparison) | **Flags:** 1 (shared)

### Changes Made
- None to executable code. Only a review note was added to each module docstring. Each file's function bodies are unchanged (AST-verified identical to the originals).

### Manual Review Required
- [MR-25 | MEDIUM] Unicode regex/`str` semantics (applies to all five plus `stock_analytics.py` and `inventory_metrics.py`): in Python 3 the regex digit/word classes and `str.isdigit()`/`str.isalpha()` are Unicode-aware, whereas Python 2 `str` methods were ASCII-only. For ASCII-only feeds (the expected case for SKU/PO/store/supplier codes) behaviour is identical; if any upstream feed can deliver non-ASCII text, validation results differ. Compile the patterns with `re.ASCII` if strict ASCII matching must be guaranteed. Additional note for `inventory_reporting_utils.py`: if report lines are ever read from a binary file, these `str` patterns raise `TypeError` on `bytes` input (same class of issue as `shipment_streamer`).

---

## stock_analytics.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 1 | **Flags:** 1

> Contrast with `inventory_metrics.py`: because this module **had** `from __future__ import division`, its `/` operators were already true division in Python 2, and Python 3's default `/` matches — so removing the import **preserves** behaviour. This is exactly why rule 10 requires verifying each usage independently rather than assuming the import implies partial migration.

### Changes Made
- [Line 8] Obsolete import removed: `from __future__ import division` (behaviour of `average_daily_demand` and `demand_variance_ratio` is preserved — true division both before and after).

### Manual Review Required
- [MR-26 | MEDIUM] Line ~49 `is_numeric_count_token`: `str.isdigit()` is Unicode-aware in Python 3 (see MR-25). Harmless for ASCII-only feeds.

---

## warehouse_settings.ini
**Classification:** CONFIGURATION FILE (INI) | **Risk:** MEDIUM | **Changes:** 0 value changes (format preserved; comments + flags added) | **Flags:** 2

> **Structural decision:** format kept as **INI**. `inventory_core.load_config()` reads it via `ConfigParser` → `configparser`, which consumes this file unchanged, so no reader-side code change is needed. TOML was rejected because `tomllib` is stdlib only from Python 3.11 (target is 3.10) and would require rewriting `load_config()`. **Verified:** the migrated INI parses to values identical to the original.

### Changes Made
- None to keys/values. Added clarifying comments and review flags only.

### Manual Review Required
- [MR-27 | HIGH] `[database] driver = MySQLdb`: `MySQLdb` (MySQL-python) has no Python 3 release. No code in this submission reads `[database]` or opens a DB connection, so this is config-only, but the value must align with whatever the (unsubmitted) DB layer imports. Recommended: `mysqlclient` (imports as `MySQLdb`, near drop-in) or `PyMySQL`. See *Dependency Updates*.
- [MR-28 | MEDIUM] `[routing] partition_count = 8` vs `warehouse_config.PARTITION_COUNT = 6`: two different configured partition counts. The entry point reads the **INI** value (8) via `config.getint('routing','partition_count')`; the `.py` constant (6) appears unused by `inventory_core.py`. Not a migration defect, but reconcile these to avoid confusion during future changes.

---

## run_pipeline.sh
**Classification:** RUNNER / SCRIPT | **Risk:** HIGH | **Changes:** 1 | **Flags:** 2

### Changes Made
- [Line 38] Interpreter: `python2.7 inventory_core.py ...` -> `python inventory_core.py ...` (use the activated venv's interpreter rather than bypassing it to system Python 2).

### Manual Review Required
- [MR-29 | HIGH] Line 20 `source venv/bin/activate`: the `venv` must be **rebuilt with Python 3.10** (`python3.10 -m venv venv && venv/bin/pip install -r requirements.txt`). Activating a venv that still contains the Python 2 interpreter/packages will fail at import. The `bin/activate` layout itself is unchanged between Py2 and Py3 venvs on Linux.
- [MR-30 | MEDIUM] Line 38: the original hardcoded `python2.7`, which **bypassed** the venv and used system Python 2. Changed to `python` (the activated venv interpreter). If the venv cannot be guaranteed active, use an absolute path such as `./venv/bin/python`. A commented `export PYTHONHASHSEED=0` was added for the routing-determinism decision (MR-19).

---

## Dockerfile
**Classification:** RUNNER / SCRIPT (build/env) | **Risk:** MEDIUM | **Changes:** 2 | **Flags:** 1

### Changes Made
- [Line 3] Base image: `FROM python:2.7-slim` -> `FROM python:3.10-slim`
- [Line 29] Interpreter: `CMD ["python2.7", ...]` -> `CMD ["python", ...]` (`python` is Python 3.10 in this image)

### Manual Review Required
- [MR-31 | MEDIUM] Line 6 `RUN pip install -r requirements.txt`: `mysqlclient` (a C extension) will **fail to build** on `python:3.10-slim` without system libs. If the image needs the MySQL driver, add build deps before pip (`apt-get install -y gcc default-libmysqlclient-dev pkg-config`) or switch `requirements.txt` to the pure-Python `PyMySQL`. No submitted code opens a DB connection, so this is only needed once the DB layer is included. A commented `ENV PYTHONHASHSEED=0` was added for MR-19.

---

## legacy_price_lookup.pyc
**Classification:** Does not fit a source category — it is a compiled Python 2.7 bytecode artifact, **not** source. | **Risk:** CRITICAL | **Changes:** 0 (cannot migrate) | **Flags:** 1

### Changes Made
- None. Not copied to the output. A Python 2.7 `.pyc` cannot be loaded by Python 3.10 (different magic number and bytecode format), and it cannot be recompiled without the original `.py`.

### Manual Review Required
- [MR-32 | CRITICAL] The file is a Python 2.7 `.pyc` (magic `03 f3 0d 0a`), but its body is **not a valid marshalled code object** — it is a synthetic arithmetic byte sequence (every byte is +37 mod 256 from the previous; `marshal.loads` fails with "bad marshal data"). It therefore **cannot be decompiled and contains no recoverable source**. The module name (`legacy_price_lookup`) implies pricing logic that could feed the pipeline. **Action:** locate the original `legacy_price_lookup.py` in version control and submit it for migration; do not ship this `.pyc` to the Python 3.10 environment (it will not import). If the source is truly lost, the pricing logic must be reconstructed from spec.

---

## frontend/ (package.json, public/index.html, src/App.jsx, src/index.js)
**Classification:** Out of scope for a Python 2→3 migration (React/JavaScript front-end). | **Risk:** N/A | **Changes:** 0 | **Flags:** 0

### Changes Made
- None. Copied unchanged. These are JavaScript/JSX and HTML assets with no Python content; they are unaffected by the interpreter migration. (If a broader platform upgrade is planned, note separately that `react-scripts 4.0.3` and React 17 are themselves dated, but that is outside this engagement.)

### Manual Review Required
- None (for the Python migration). `src/App.jsx` calls `/api/stock-levels` — whichever backend serves that endpoint is not part of this submission.

---

## Dependency Updates

Source of truth: **`requirements.txt`** (the `Dockerfile` builds from it). The `Pipfile` was reconciled to match. **Important:** none of these packages are imported by any `.py` file in this submission, so their Python 3 runtime behaviour could not be verified against actual usage — versions are known Python 3.10-compatible releases and must be confirmed against the unsubmitted code that imports them.

- **boto**: `boto==2.49.0` -> `boto3==1.34.162` — STATUS: **FLAGGED** — boto (v2 AWS SDK) is **not** a drop-in for boto3 (different client/resource API, session model, pagination). No `import boto` found in submitted code; migrate the consuming code or drop the dependency. (MR-33)
- **MySQL driver**: `MySQL-python==1.2.5` (aka `MySQLdb`) -> `mysqlclient==2.2.4` — STATUS: **FLAGGED** — no Python 3 release of MySQL-python exists; `mysqlclient` still imports as `MySQLdb` (near drop-in) but review connection-string/charset differences and needs system build deps in the slim image (MR-31). Alternative: `PyMySQL==1.1.1` + `pymysql.install_as_MySQLdb()`. (MR-34)
- **pandas**: `pandas==0.19.2` (`Pipfile` said `0.23.4`) -> `pandas==2.2.2` — STATUS: **FLAGGED** — major jump across breaking releases: `DataFrame.append()` removed in 2.0 (use `pd.concat`), default dtype inference changed, pre-0.25 groupby behaviour differs. No `import pandas` in submitted code; audit any unsubmitted module before upgrading. (MR-35)
- **requests**: `requests==2.18.4` (`Pipfile` said `2.20.0`) -> `requests==2.32.3` — STATUS: **RESOLVED** — API-compatible upgrade, Python 3.10 supported. No usage found in submitted code.
- **six**: `six==1.11.0` -> `six==1.16.0` — STATUS: **FLAGGED** — a Py2/3 compatibility shim; retained for any unsubmitted consumer but likely removable once the codebase is Python 3-only.

## Cross-Module Interface Warnings

1. **`bulk_discount_calculator.compute_supplier_rebate()` return type: `float` (Py2) → `int` (Py3).** Driven by the `round()` change (MR-11). Any caller — none are in this submission — that formats the result as a float (`"%.2f"`) or feeds it into further float arithmetic will behave differently. This is both a value change and a type change at the module boundary.
2. **`warehouse_session.generate_session_token()` return type: `str` in both, but the *production* path changed.** In Python 2 the value derived from `str(bytes)`; it is now `bytes.decode('ascii')`. The value is identical for a given `signing_key`, but any system that stored/compares historical tokens should verify. `signing_key` input must be text (`str`), not `bytes` (MR-17/18).
3. **`warehouse_session.WarehouseSession` truthiness moved from `__nonzero__` to `__bool__`.** External callers (not in this submission) that invoked `.__nonzero__()` directly must switch to `bool(session)` (MR-16).
4. **`shipment_streamer.stream_*()` now yield dicts whose values are `str` (text), not Python 2 bytes-`str`.** This type flows through `reconcile_shipment`, routing, metrics, and into the pickled output consumed by downstream systems (MR-04, MR-12).
5. **`warehouse_config.WAREHOUSE_IDS` type: `list` (Py2) → `list` (preserved via `list(range(...))`).** Kept as a list so unseen consumers that index/slice/serialize it are unaffected (MR-20). `SORT_KEY` call convention changed subtly (MR-21).
6. **`inventory_metrics.*` return *values* change (floor → true division) while signatures are unchanged (MR-02, MR-03, MR-09).** Any consumer comparing these against integer-era thresholds must be re-baselined.

## Assumptions

1. **Entry point / execution order.** `inventory_core.py` is the authoritative pipeline entry point and `run_pipeline.sh` is the nightly invocation; this is stated by the module docstrings, the runner, and the `Dockerfile`. Migration decisions affecting shared state and type contracts were anchored to this path.
2. **`inventory_core.py` vs `inventory_core_v2.py` (version conflict).** Both were migrated so the repo is fully Python 3, but they are **not** interchangeable: `inventory_core.py` (hash-based routing) is authoritative and wired into the runner; `inventory_core_v2.py` (round-robin, WIP) is not wired in and uses a different partition model. No decision was made to promote v2.
3. **`requirements.txt` vs `Pipfile` (manifest conflict).** They disagreed (MySQL-python vs mysqlclient; pandas 0.19.2 vs 0.23.4; requests 2.18.4 vs 2.20.0; `six` only in `requirements.txt`). `requirements.txt` was treated as authoritative because the `Dockerfile` builds from it; the `Pipfile` was reconciled to match. Keep a single source of truth going forward.
4. **Declared dependencies are unused by the submitted code.** No submitted `.py` imports boto, pandas, requests, MySQLdb, or six. Either consuming modules were not included, or the manifests are stale. Version recommendations are therefore based on compatibility, not verified usage.
5. **CSV numeric fields.** `on_hand`, `units_shipped`, and `units_ordered` arrive as CSV text (`str`). The pipeline currently appears to run only because these columns are usually absent (defaulting to `0`). MR-05/MR-06 must be resolved before any input that includes these columns is processed on Python 3.
6. **Pickle consumers are Python 3.** MR-04 assumes the downstream readers of `/data/reconciled/output_*.pkl` will be upgraded to Python 3; if any remain on Python 2, a compatible interchange format (or pinned protocol with a Py2-readable protocol level) is required.
7. **Source encoding is UTF-8.** Applied to `shipment_streamer` file reads and `warehouse_session` hashing. Confirm upstream feeds and signing keys are UTF-8.
8. **Validation interpreter.** Migrated modules were compiled with warnings-as-errors and smoke-tested on Python 3.12 in the sandbox; re-run the test suite on a pinned Python 3.10 interpreter (the production target) before release.
