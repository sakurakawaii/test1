# Migration Report

**Submission Date:** 2026-07-18 | **Overall Risk:** CRITICAL
**Files Processed:** 25 | **Changes Applied:** 73 | **Review Flags:** 33

> Scope: Python 2.7 -> Python 3.10 migration of the nightly inventory reconciliation pipeline.
> 20 files were migrated/converted (15 `.py`, 1 `.ini`, 2 manifests, `run_pipeline.sh`, `Dockerfile`).
> 5 files were classified but NOT migrated (4 non-Python frontend assets, 1 compiled `.pyc` with no source) and are documented at the end.
> "Changes Applied" counts distinct logical edits, each annotated in-source with `# PY3-MIGRATED`. Several edits carry a multi-line rationale block, so a raw grep of the tag returns a higher number (98). All human-review points are annotated in-source with `# PY3-REVIEW` and enumerated below as MR items.

### Dependency & Execution Graph (established before migration)
```
run_pipeline.sh / Dockerfile
        └── inventory_core.py        (AUTHORITATIVE entry point)
                ├── stock_router          (route_to_partition)
                ├── sku_classifier        (get_route)
                ├── warehouse_session     (WarehouseSession, generate_session_token)
                ├── warehouse_config      (DEFAULT_TIMEOUT)            [Python-based config]
                ├── inventory_metrics     (count_stockout_events, compute_fill_rate_ratio)
                └── shipment_streamer     (stream_shipments)

inventory_core_v2.py  (WIP, NOT wired into runner) ── shipment_streamer
```
Standalone shared utilities with no first-party importer in this submission (assumed consumed by un-submitted callers): `inventory_reporting_utils`, `stock_analytics`, `sku_validator`, `store_validator`, `supplier_contact_validator`, `purchase_order_validator`, `bulk_discount_calculator`.
Migration order followed: shared utilities first, then the core entry points.

---

## inventory_core.py
**Classification:** PIPELINE MODULE (authoritative entry point) | **Risk:** CRITICAL | **Changes:** 13 | **Flags:** 5

### Changes Made
- [Line 1] Interpreter: `#!/usr/bin/env python2.7` -> `#!/usr/bin/env python3` (annotation kept off the shebang line deliberately)
- [Line 21] stdlib rename: `import cPickle as pickle` -> `import pickle`
- [Line 22] stdlib rename: `import ConfigParser` -> `import configparser`
- [Line 37] API: `ConfigParser.ConfigParser()` -> `configparser.ConfigParser()`
- [Line 50] Membership: `buckets.has_key(bucket)` -> `bucket not in buckets`
- [Line 66] Division: `return total_records / partition_count` -> `return total_records // partition_count` (see MR-02)
- [Line 75] Exception: `except ValueError, e:` -> `except ValueError as e:`
- [Line 77] Print: `print >> sys.stderr, "Bad unit_cost..."` -> `print("...", file=sys.stderr)`
- [Line 98] Raise: `raise Exception, "..."` -> `raise Exception("...")`
- [Line 106] Iteration: `buckets.iteritems()` -> `buckets.items()` (dict not mutated in loop; safe)
- [Line 108] Print: `print "Processing partition..."` -> `print("...")`
- [Line 144] Print: `print "Reconciliation complete..."` -> `print("...")`
- [Line 150] Print: `print >> sys.stderr, "usage..."` -> `print("...", file=sys.stderr)`

### Manual Review Required
- [MR-05 | CRITICAL] Lines 112, 119, 125: `sum(1 for r in reconciled if r.get('on_hand', 0) <= 0)` and `sum(r.get('units_shipped', 0) ...)`. Record values now arrive as `str` from `shipment_streamer` (see MR-04). If the feed contains an `on_hand` column, `'5' <= 0` raises `TypeError` in Python 3 (reproduced in testing); Python 2 silently returned `False` and never counted a stockout. If `units_shipped`/`units_ordered` columns are present, `sum()` starting at int `0` raises `TypeError` in both versions. Action: coerce these fields to `int` inside `reconcile_shipment` (e.g. `int(record.get('on_hand') or 0)`) before the aggregation, and decide the intended semantics for missing/blank values.
- [MR-03 | CRITICAL] Line 141: `pickle.dump({...}, out)` writes with Python 3's default protocol (>=3), which **no Python 2 reader can load**. The pickled payload also changed shape: record values are now `str` (were `bytes`), and `summary['stockout_ratio']`/`['fill_rate']` are now `float` (were `int`; see MR-02). Action: confirm every downstream consumer of `/data/reconciled/*.pkl` is Python 3; if any is Python 2, pass `protocol=2` AND validate the str/float type changes, or switch the hand-off to JSON.
- [MR-02 | CRITICAL] Line 66: `average_batch_size` changed `/` to `//` to preserve the Python 2 integer result for this batch-count field. Verified `avg_batch_size` remains `int` in the summary. Action: confirm the ops-log summary consumer expects an integer; if a true fractional average is wanted, revert to `/` (float) and update that consumer.
- [MR-07 | CRITICAL] Line 97: `if not session:` depends on `WarehouseSession.__bool__`, renamed from `__nonzero__` in `warehouse_session.py`. If that rename is ever reverted, this auth guard silently becomes always-false and the pipeline runs without an authenticated session. Action: keep a unit test asserting `bool(WarehouseSession(..., token=''))` is `False`.
- [MR-06 | CRITICAL] Line 51/`partition_batch`: partition assignment comes from `stock_router.route_to_partition` whose hash implementation changed (see MR-06 under stock_router.py). Within this module the final reconciled output is independent of bucket identity, but the per-partition log lines and any downstream use of bucket IDs will differ from Python 2.

---

## inventory_core_v2.py
**Classification:** PIPELINE MODULE (WIP rewrite, NOT wired into the runner) | **Risk:** LOW | **Changes:** 4 | **Flags:** 0

### Changes Made
- [Line 1] Interpreter: `python2.7` -> `python3` shebang
- [Line 30] Membership: `buckets.has_key(bucket)` -> `bucket not in buckets`
- [Line 40] Iteration: `buckets.iteritems()` -> `buckets.items()` (dict not mutated; safe)
- [Line 42] Print: `print "partition %d..."` -> `print("...")`

### Manual Review Required
- [MR-17 | MEDIUM] This is a second version of the entry point. It was migrated for completeness but **must not** be wired into `run_pipeline.sh`/`Dockerfile`; `inventory_core.py` remains authoritative. See Assumptions #1. Its `round_robin_partition` does not carry the hash-determinism risk (it uses `i % partition_count`), so it is low risk on its own, but it omits the auth/session gate and metrics present in `inventory_core.py`.

---

## inventory_metrics.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 2 | **Flags:** 5

### Changes Made
- [Line 14] Regex: `re.compile(r'^[a-z_]+\.\w+$')` -> added `re.ASCII` (preserve Python 2 ASCII `\w`)
- [Line 15] Regex: `re.compile(r'^\d+(\.\d+)?$')` -> added `re.ASCII` (preserve Python 2 ASCII `\d`)

### Manual Review Required
- [MR-02 | CRITICAL] Lines 43, 54, 62, 68, 74: all five functions use `/` with **no** `from __future__ import division`, so in Python 2 they performed **integer** division and returned `int`; in Python 3 they perform **true** division and return `float`, with different numeric values (e.g. `3/2` was `1`, now `1.5`; `97/100` was `0`, now `0.97`). These feed nightly stockout/fill-rate/turnover/forecast alerts compared against fractional floors (`0.95`, `0.80`, `0.90`), so true division is the semantically correct behavior, but it is a **silent change in both return type and value** versus the pre-migration output. Action: (1) confirm alert thresholds were authored for the true-division scale, (2) re-baseline any stored historical metric values, (3) see the Cross-Module Interface Warnings for the return-type contract change affecting all callers. `//` was intentionally NOT applied because floor division on a ratio compared to `0.95` is meaningless.

---

## stock_router.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 2 | **Flags:** 1

### Changes Made
- [Line 8] Added `import hashlib` to support a process-stable hash
- [Line 32] Routing: `hash(str(sku)) % partition_count` -> `_stable_partition_hash(sku) % partition_count` (original line preserved in a comment block above)

### Manual Review Required
- [MR-06 | CRITICAL] Line 32: Python 3 salts the builtin `hash()` of `str` per process (`PYTHONHASHSEED`), so `hash(str(sku))` is **not stable across runs/processes** - directly contradicting the module's documented "deterministic / stable-hash routing" and the `hash_seed_pinned = false` setting. Reproduced: two separate interpreters returned different `hash('SKU0')` values. The migration replaces the builtin hash with an `md5`-based content hash that is deterministic across processes AND Python versions (verified: identical output across two interpreters). **Consequence:** the partition a given SKU maps to now differs from the Python 2 builtin-hash result. Action: confirm no downstream system persisted or sharded storage on the Python 2 partition numbers; if one did, it must be re-keyed. If instead the team prefers to keep builtin `hash()`, you must export `PYTHONHASHSEED=0` in `run_pipeline.sh` and the Dockerfile and accept that values still differ from Python 2.

---

## shipment_streamer.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 4 | **Flags:** 3

### Changes Made
- [Line 21] File mode: `csv.reader(open(path, 'rb'))` -> `csv.reader(open(path, 'r', newline=''))` (Python 3 csv requires text mode)
- [Line 29-35] `stream_shipments`: `source_iterator.next()` -> `next(source_iterator)`, and `while True: ... .next()` -> `for row in source_iterator:` with an empty-source guard
- [Line 48-52] `stream_with_index`: same `.next()` and loop refactor using `enumerate`
- [Line 59-64] `stream_chunked_by_warehouse`: same `.next()` and loop refactor

### Manual Review Required
- [MR-04 | CRITICAL] Line 21: opening the CSV in binary (`'rb'`) and handing it to `csv.reader` raises `"iterator should return strings, not bytes"` in Python 3. Switched to text mode with `newline=''`. **Boundary effect:** every field value now decodes to `str`, where Python 2 produced `bytes`. This type flows through the entire pipeline (`reconcile_shipment`, the aggregations in MR-05, and the pickled output in MR-03). Action: confirm the source encoding is UTF-8; if it is latin-1/cp1252, pass `open(path, 'r', newline='', encoding='...')` explicitly to avoid `UnicodeDecodeError`.
- [MR-18 | HIGH] Lines 29, 35 (and the other two readers): the original `while True: row = it.next()` relied on `StopIteration` propagating to end the generator. Under PEP 479 (Python 3.7+) a `StopIteration` raised **inside** a generator is converted to `RuntimeError` (reproduced). The loops were rewritten to `for`-loops, which terminate cleanly. Action: none required beyond review - verified empty-file inputs now yield zero records instead of crashing.
- [MR-09 | HIGH] Lines 64-70: `stream_chunked_by_warehouse` still drops a trailing partial chunk (< `chunk_size`), preserving the original Python 2 behavior (which also dropped it). Verified: 3 rows at `chunk_size=2` yields one chunk of 2 and discards the last row. Action: if the final partial batch should be processed, add `if chunk: yield chunk` after the loop - but confirm this with the data owner, as it changes record counts downstream.

---

## warehouse_session.py
**Classification:** UTILITY / HELPER | **Risk:** CRITICAL | **Changes:** 4 | **Flags:** 2

### Changes Made
- [Line 26] Truthiness: `def __nonzero__(self):` -> `def __bool__(self):`
- [Line 40] `is_expired`: `return not self.__nonzero__()` -> `return not bool(self)`
- [Line 51] Hashing: `hashlib.sha256(signing_key + payload)` -> `hashlib.sha256((signing_key + payload).encode('utf-8'))`
- [Line 55] Token: `return str(signature)` -> `return signature.decode('ascii')`

### Manual Review Required
- [MR-07 | CRITICAL] Line 26: `__nonzero__` is **ignored** in Python 3; without the rename to `__bool__`, every `WarehouseSession` is unconditionally truthy and the `if not session:` auth guard in `inventory_core.py` silently stops firing. Verified after rename: empty-token session is falsy, valid session is truthy. Action: retain a regression test (see MR-07 in inventory_core.py).
- [MR-08 | CRITICAL] Lines 51 & 55: two str/bytes defects fixed together. (1) `hashlib.sha256()` requires `bytes` in Python 3 - passing `str` raises `TypeError`. (2) `str(signature)` on a `bytes` object in Python 3 returns the literal repr `"b'...'"`, producing a corrupted token; `.decode('ascii')` is required. Verified: token is now clean base64 (`Le41...SUE=`, not prefixed with `b'`). **Assumption:** the signing key is ASCII, so the utf-8-encoded digest equals the Python 2 byte-string digest and tokens remain stable across the migration. Action: if `signing_key` may be non-ASCII, the Python 2 and Python 3 tokens will differ - confirm and, if needed, document a token rotation at cutover.

---

## warehouse_config.py
**Classification:** CONFIGURATION FILE (Python-based) | **Risk:** HIGH | **Changes:** 5 | **Flags:** 0

### Structural decision
This file mixes declarative constants with executable logic (`is_known_warehouse`, the `SORT_KEY` lambda, and an import-time `print`) and is consumed via `import warehouse_config`. Converting it to a static format (INI/TOML/YAML) would break that import contract and drop the helper/lambda. **Decision:** keep it as a Python module and migrate in place. (Recommendation for a future pass: move the purely declarative constants into `warehouse_settings.ini` and leave only logic here, but that is an API change and out of scope for this migration.)

### Changes Made
- [Line 11] Sequence: `WAREHOUSE_IDS = range(1, 25)` -> `list(range(1, 25))` (Python 3 `range` is lazy; preserve list semantics)
- [Line 15] Literal: `DEFAULT_TIMEOUT = 30L` -> `30` (the `L` long suffix is a `SyntaxError` in Python 3)
- [Line 29] Lambda: `SORT_KEY = lambda (code, qty): qty` -> `lambda item: item[1]` (tuple-unpacking params removed, PEP 3113 - was a `SyntaxError`)
- [Line 36] Type check: `isinstance(value, basestring)` -> `isinstance(value, str)` (`basestring` removed)
- [Line 43] Print: `print '...'` -> `print('...')` (import-time side effect preserved)

### Manual Review Required
- [MR-16 | MEDIUM] Line 43: the module prints to stdout at import time. This is preserved, but it will now appear in Python 3 logs/captured output (reproduced in the end-to-end run). Confirm this is acceptable, or gate it behind `if __name__ == '__main__':` / logging. Also note `SORT_KEY`'s signature contract change in Cross-Module Interface Warnings, and that `WAREHOUSE_IDS` is now a concrete `list` (callers relying on list ops are safe; this is intentional).

---

## inventory_reporting_utils.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 4 | **Flags:** 2

### Changes Made
- [Lines 14-17] Regex: added `re.ASCII` to `REPORT_LINE_PATTERN`, `HEADER_PATTERN`, `NUMERIC_FIELD_PATTERN`, `TRAILING_SPACE_PATTERN` to preserve Python 2 ASCII-only `\w`/`\d`/`\s`.

### Manual Review Required
- [MR-14 | MEDIUM] Line 26: `quantity.isdigit()` is Unicode-aware in Python 3; the `re.ASCII` `\d` group backstops it so only ASCII digits reach it, matching Python 2. Confirm the warehouse report feed is ASCII fixed-width. (`findall` still returns a list - no iterator change - so `extract_numeric_fields` callers are unaffected.)

---

## sku_validator.py
**Classification:** UTILITY / HELPER | **Risk:** MEDIUM | **Changes:** 5 | **Flags:** 2

### Changes Made
- [Lines 15-19] Regex: added `re.ASCII` to `SKU_PATTERN`, `LOT_CODE_PATTERN`, `BIN_LOCATION_PATTERN`, `QUANTITY_TOKEN_PATTERN`, `WHITESPACE_TRIM_PATTERN` (preserve Python 2 ASCII semantics for structured codes)

### Manual Review Required
- [MR-14 | MEDIUM] Line 20 & 39: `DESCRIPTION_ALLOWED_PATTERN` was intentionally left Unicode-aware (`\w`/`\s`) because free-text descriptions may legitimately contain accented characters; confirm this is desired or add `re.ASCII`. Verified: `is_valid_sku` now rejects fullwidth-digit SKUs (e.g. `AB\uff11\uff12\uff13456`), matching Python 2. `is_valid_quantity_token` uses Unicode-aware `str.isdigit()` backstopped by the `re.ASCII` regex, so its boolean result is unchanged from Python 2.

---

## store_validator.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 4 | **Flags:** 1

### Changes Made
- [Lines 13-16] Regex: added `re.ASCII` to `STORE_CODE_PATTERN`, `DC_CODE_PATTERN`, `REGION_CODE_PATTERN`, `TRANSFER_REF_PATTERN`

### Manual Review Required
- [MR-14 | MEDIUM] Line 30: `is_valid_region_code` combines Unicode-aware `str.isalpha()` with an `re.ASCII` `[A-Z]` regex; the regex backstops the method so the result is ASCII-only as in Python 2. Confirm region codes are always ASCII.

---

## supplier_contact_validator.py
**Classification:** UTILITY / HELPER | **Risk:** MEDIUM | **Changes:** 4 | **Flags:** 2

### Changes Made
- [Lines 16-19] Regex: added `re.ASCII` to `EMAIL_PATTERN`, `PHONE_PATTERN`, `NAME_PATTERN`, `POSTAL_CODE_PATTERN`

### Manual Review Required
- [MR-14 | MEDIUM] Line 16 (email): `re.ASCII` preserves Python 2 behavior but rejects internationalized (EAI / non-ASCII) email addresses. Confirm with the onboarding team whether international supplier emails must be accepted; if so, drop `re.ASCII` from `EMAIL_PATTERN`.
- [MR-14b | MEDIUM] Line 33 (name): `str.isalpha()` is Unicode-aware in Python 3 (e.g. "José" passes), but the `re.ASCII` `[A-Za-z]` `NAME_PATTERN` still rejects accented names, so the combined result stays ASCII-only. Decide deliberately whether international supplier names should be accepted; if yes, relax the `isalpha()` check and the pattern **together**.

---

## purchase_order_validator.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 4 | **Flags:** 1

### Changes Made
- [Lines 13-16] Regex: added `re.ASCII` to `PO_NUMBER_PATTERN`, `LINE_ITEM_COUNT_PATTERN`, `CURRENCY_AMOUNT_PATTERN`, `SUPPLIER_REF_PATTERN`

### Manual Review Required
- [MR-14 | MEDIUM] Line 22: `count_str.isdigit()` is Unicode-aware in Python 3, backstopped by the `re.ASCII` `\d` regex so the boolean is unchanged from Python 2. Confirm EDI feeds are ASCII.

---

## stock_analytics.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 3 | **Flags:** 1

### Changes Made
- [Line 9] Removed obsolete `from __future__ import division`. **Verified independently:** this module already used true division in Python 2 via that import, and Python 3 `/` is true division, so `average_daily_demand` and `demand_variance_ratio` behavior is **unchanged** (this is the one division-bearing module that does NOT drift - contrast with `inventory_metrics.py`).
- [Lines 13-14] Regex: added `re.ASCII` to `COUNT_FIELD_PATTERN`, `DEMAND_CODE_PATTERN`

### Manual Review Required
- [MR-14 | MEDIUM] Line 38: `is_numeric_count_token` uses Unicode-aware `str.isdigit()` with no regex backstop in this function. A non-ASCII decimal digit would return `True` where Python 2 (byte strings) returned `False`. Add an explicit ASCII guard if upstream feeds can contain non-ASCII input.

---

## bulk_discount_calculator.py
**Classification:** UTILITY / HELPER (finance-sensitive) | **Risk:** CRITICAL | **Changes:** 0 | **Flags:** 2

### Changes Made
- No code changed. The computation line is preserved intact because the module's header mandates Finance sign-off before any rounding change. The ready-to-enable Python 2-equivalent implementation is included as a commented block at the top of the file.

### Manual Review Required
- [MR-01 | CRITICAL] Line 49: `return round(raw_rebate)`. The docstring claims rounding is "stable across Python versions" - this is **false**. Python 2 `round()` rounds halves away from zero; Python 3 uses banker's rounding (round-half-to-even). With the tier rates this silently changes supplier rebates by $1 at half-dollar boundaries. **Reproduced:** `compute_supplier_rebate(105)` returns `10` under Python 3 vs `11` under Python 2; `units=1005` returns `502` vs `503`. This directly affects money owed to suppliers and will not raise an exception. Action (requires Finance sign-off): enable the `decimal.Decimal` + `ROUND_HALF_UP` implementation provided in-file, which also removes the binary-float error in `units * rate` (0.1 is not exactly representable). Do NOT ship this module to production until Finance confirms the intended rounding.

---

## sku_classifier.py
**Classification:** UTILITY / HELPER | **Risk:** LOW | **Changes:** 0 | **Flags:** 0

### Changes Made
- Reviewed line by line; no Python 2-specific constructs (no `print` statement, integer division, `iteritems`/`has_key`, exception-comma syntax, or str/bytes mixing). Category string comparisons are unaffected by the bytes->str change because both the CSV values (now `str`) and the dict literals are text. A top-of-file note documents the clean review. Output is functionally identical to the input.

---

## warehouse_settings.ini
**Classification:** CONFIGURATION FILE | **Risk:** LOW | **Changes:** 0 | **Flags:** 3

### Structural decision
INI is retained - Python 3 `configparser` reads the file unchanged, so no format conversion is needed. All notes are placed on their own comment lines (configparser does not enable inline end-of-line comments by default), and no value contains a `%` that `BasicInterpolation` would try to expand. The `[database] driver` value was **intentionally left as `MySQLdb`** because the recommended replacement library (`mysqlclient`) still exposes that import name.

### Manual Review Required
- [MR-15 | MEDIUM] `[routing] hash_seed_pinned = false`: now moot because migrated `stock_router.py` uses a content hash (see MR-06). If the team reverts to builtin `hash()`, this must become `true` and `PYTHONHASHSEED` pinned in the runner/Docker env.
- [MR-13 | HIGH] `[database]`: no code in this submission reads this section, so the `driver`/`host`/`port` values are consumed only by a DB-access module not included here. Reconcile the `driver` value and connection arguments with that module during the dependency migration (see Dependency Updates).

---

## requirements.txt
**Classification:** DEPENDENCY MANIFEST (authoritative - used by Dockerfile) | **Risk:** HIGH | **Changes:** 5 | **Flags:** 0
See **Dependency Updates** below for per-package detail. This file is authoritative for the container build; `Pipfile` was reconciled to match it.

## Pipfile
**Classification:** DEPENDENCY MANIFEST | **Risk:** HIGH | **Changes:** 6 | **Flags:** 0
Reconciled to match `requirements.txt` and retargeted to `python_version = "3.10"`. The original disagreements with `requirements.txt` are logged under Assumptions #2. See **Dependency Updates**.

---

## run_pipeline.sh
**Classification:** RUNNER / SCRIPT | **Risk:** MEDIUM | **Changes:** 1 | **Flags:** 2

### Changes Made
- [Line ~40] Interpreter: `python2.7 inventory_core.py ...` -> `python inventory_core.py ...` (uses the activated venv's interpreter, now Python 3.10)

### Manual Review Required
- [MR-15 | MEDIUM] `source venv/bin/activate`: the `./venv` virtualenv must be **rebuilt** with Python 3.10 (`python3.10 -m venv venv && venv/bin/pip install -r requirements.txt`) before this runner is used. The `bin/activate` layout is identical under Python 3, so the line is unchanged, but a venv still containing Python 2 would silently run the old code. Environment assumption: `cwd` is prepended to `PYTHONPATH` so the top-level modules resolve as absolute imports (this is why `import stock_router` still works and is NOT an implicit-relative-import problem).
- [MR-03 | CRITICAL] The `.pkl` produced here is now Python 3-protocol pickle containing str/float values; any Python 2 reader of `/data/reconciled/*.pkl` will fail. See MR-03 under inventory_core.py.

---

## Dockerfile
**Classification:** RUNNER / SCRIPT (container build/runtime) | **Risk:** MEDIUM | **Changes:** 3 | **Flags:** 1

### Changes Made
- [Line 2] Base image: `FROM python:2.7-slim` -> `FROM python:3.10-slim`
- [Lines 6-13] Added `apt-get install gcc pkg-config default-libmysqlclient-dev` - `mysqlclient` is a C extension needing build/runtime libs that the old install did not
- [Line ~24] Entrypoint: `CMD ["python2.7", ...]` -> `CMD ["python3", ...]`

### Manual Review Required
- [MR-13 | HIGH] The added build dependencies are required for `mysqlclient`. If the team switches to `PyMySQL` (pure Python), remove the `apt-get` layer. Consider a multi-stage build so `gcc`/`pkg-config` are not shipped in the final image. Verify the image builds in CI before cutover (not verifiable in this sandbox - no network access).

---

## Dependency Updates

- **boto** `==2.49.0` -> **boto3** `==1.34.131` - STATUS: FLAGGED (HIGH) - boto v2 is EOL and Python 2-oriented; boto3 is **not a drop-in replacement** (entirely different client/resource/session API). No submitted module imports `boto`, so usage lives in un-submitted code that must be rewritten call-by-call. Do not assume a mechanical swap.
- **MySQL-python / MySQLdb** `==1.2.5` -> **mysqlclient** `==2.2.4` - STATUS: FLAGGED (HIGH) - `MySQL-python` does not install on Python 3. `mysqlclient` is the maintained fork and keeps the `import MySQLdb` name (so `warehouse_settings.ini driver = MySQLdb` stays valid), but: (a) it is a C extension needing system build deps (added to the Dockerfile); (b) connection-argument defaults differ (`charset`, `use_unicode`, SSL options) and query results now return `str`/`bytes` differently than Python 2 - verify the (un-submitted) DB module's connect call and result handling. Pure-Python alternative: **PyMySQL** `==1.1.1` (`import pymysql`, or `pymysql.install_as_MySQLdb()`), no build deps.
- **pandas** `==0.19.2` (req) / `==0.23.4` (Pipfile) -> **pandas** `==1.5.3` - STATUS: FLAGGED (HIGH) - chose 1.5.x over 2.x to limit behavioral change. Breaking changes to verify in any (un-submitted) pandas code before a later 2.x bump: `DataFrame.append` is **removed** in 2.0, `.iteritems()` removed, default dtype inference changed, and pre-0.25 `groupby` patterns changed. No pandas usage in submitted code.
- **requests** `==2.18.4` (req) / `==2.20.0` (Pipfile) -> **requests** `==2.32.3` - STATUS: RESOLVED - Python 3.10 compatible; no submitted usage. Note responses: `resp.content` is `bytes`, `resp.text` is `str` - ensure downstream (un-submitted) code does not feed `.read()`/`.content` straight into `json.loads` without decoding.
- **six** `==1.11.0` -> **six** `==1.16.0` - STATUS: FLAGGED (advisory) - compatibility shim; safe to keep and update, but removable once all `six` usage is gone. Absent from the original Pipfile; added there for parity. No submitted usage.

---

## Cross-Module Interface Warnings

1. **inventory_metrics.py return types (int -> float).** `count_stockout_events`, `count_reorder_multiples`, `compute_fill_rate_ratio`, `compute_turnover_ratio`, and `compute_forecast_accuracy_ratio` now return `float` (were `int` for integer inputs in Python 2). Any caller - including ones not in this submission - that uses these results as a dict key, list index, `isinstance(..., int)` check, or feeds them into further integer division will behave differently. `inventory_core.py` stores two of them in the pickled summary (see MR-03).
2. **shipment_streamer.py field value types (bytes -> str).** All four stream readers now yield records whose values are `str`. Any consumer that did byte-level operations (e.g. `.startswith(b'...')`, byte slicing, writing to a binary sink) must be updated.
3. **warehouse_session.generate_session_token** return type is `str` in both versions (contract stable), but the **internal** token value is only guaranteed identical to Python 2 for ASCII signing keys (see MR-08).
4. **warehouse_session.WarehouseSession** truthiness now routes through `__bool__`. Any caller using `bool(session)` / `if session:` / `if not session:` depends on the rename; the behavior is preserved only because the rename was applied (MR-07).
5. **stock_router.route_to_partition** return value (the partition index for a given SKU) changed versus Python 2 (MR-06). Signature is unchanged; the mapping is not.
6. **warehouse_config.SORT_KEY** signature changed from a two-arg-unpacking lambda to a single-tuple-arg lambda `lambda item: item[1]`. Callers invoking it as `key=SORT_KEY` over `(code, qty)` pairs are unaffected; any caller that called it as `SORT_KEY(code, qty)` (two positional args) would break and must use `SORT_KEY((code, qty))`.
7. **warehouse_config.WAREHOUSE_IDS** is now a concrete `list` (was already list-like in Python 2); `DEFAULT_TIMEOUT` is now a plain `int` (was `long`). Both are consumed as-is by `inventory_core.py`.

---

## Assumptions

1. **Two entry-point versions exist.** `inventory_core.py` is treated as the authoritative, runner-wired entry point (per its docstring and `run_pipeline.sh`/`Dockerfile`), and `inventory_core_v2.py` as a non-wired WIP rewrite. Both were migrated, but they are NOT interchangeable; v2 omits the session/auth gate and metrics and uses round-robin instead of hash routing. Do not wire v2 into the runner without the team's pending validation.
2. **Manifest conflict (requirements.txt vs Pipfile).** The two manifests disagreed: `MySQL-python==1.2.5` vs `mysqlclient==1.4.2`, `pandas==0.19.2` vs `0.23.4`, `requests==2.18.4` vs `2.20.0`, and `six` present only in `requirements.txt`. `requirements.txt` was treated as authoritative because the `Dockerfile` installs from it; `Pipfile` was reconciled to match. Confirm this is the intended source of truth.
3. **CSV source encoding is UTF-8** and the numeric-looking columns either arrive pre-typed or are absent in the production feed. In testing, a feed containing a raw `on_hand` column triggers a `TypeError` in Python 3 (MR-05); the "happy path" feed without `on_hand`/`units_*` columns runs end-to-end. The correct typing of these fields must be confirmed with the data owner.
4. **The `signing_key` is ASCII**, so migrated session tokens match Python 2 (MR-08).
5. **No downstream system persisted Python 2 partition numbers** from `stock_router`, and no Python 2 process reads the output `.pkl` (MR-06, MR-03). If either is false, additional remediation is required.
6. **`legacy_price_lookup.pyc` is not imported** by any submitted module (confirmed by grep) and its source is unavailable, so it was not migrated (see below).
7. **Standalone validators / analytics utilities are consumed by modules not in this submission.** Their interfaces were held stable and all Unicode-semantics decisions (`re.ASCII`) were made to preserve Python 2 behavior; confirm no caller requires non-ASCII input (MR-14).
8. **Execution order within a single run:** `warehouse_config` prints at import time, and module import order is driven by `inventory_core.py`'s import block. No shared mutable state crosses module boundaries at import time other than that print, so import order does not affect correctness.

---

## Files Classified but NOT Migrated

- **legacy_price_lookup.pyc** - Compiled Python 2.7 bytecode (magic `03f30d0a`), 408 bytes, **no source provided**. Does not fit a source category. Python 3 cannot load or unmarshal Python 2 bytecode (confirmed: `ValueError: bad marshal data`), and decompilation cannot guarantee a correct `.py`. **[MR-10 | HIGH]** Action: obtain the original `legacy_price_lookup.py` from version control and submit it for migration. Any module that imports it will fail under Python 3; no submitted module does, so it is currently dormant but must not be deployed as-is.
- **frontend/** (`package.json`, `public/index.html`, `src/App.jsx`, `src/index.js`) - Non-Python React UI assets. Out of scope for a Python 2->3 migration; left unchanged. **Interface note:** `App.jsx` fetches `GET /api/stock-levels` and renders fields `item.sku` and `item.onHand` (camelCase). No backend API module is present in this submission; if one is added later, its JSON must expose `sku` and `onHand` with JSON-serializable (str/number) values. Note the pipeline currently emits a pickle, not this JSON API, so the API layer is elsewhere.
