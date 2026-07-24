# Test Report — `dateutils`

## Summary

| Metric | Result |
|---|---|
| Tests | **177 passed, 7 xfailed** (suggested features), 0 failures |
| Line + branch coverage (full suite, incl. reject-verification) | **100% / 100%** (410 stmts, 88 branches) |
| Line + branch coverage (standard tests only) | 94% — the missing 6% is exactly the rejected defect regions listed below |
| Defects found | **8 rejected behaviors** (D1–D8), 23 `reject_verification` tests proving them |
| Suggested features | 7 (S1–S7), each with `xfail`-marked tests ready to flip green |

Run with:

```bash
pip install pytest pytest-cov pytest-mock
python -m pytest tests --cov=dateutils --cov-branch            # full suite → 100%/100%
python -m pytest tests -m "not reject_verification"            # expected behavior only
python -m pytest tests -m static                               # static/class-level method tests
python -m pytest tests -m feature_calendar_math                # per-feature selection
```

---

## ⚠️ Critical finding first (D1)

**As shipped, `Month`, `Weekday`, `Season` and `Hour` cannot be instantiated at all** — not from ints, not from names. The module targets Python 3.12+ and uses PEP 695 lazy type aliases (`type MonthName = Literal[...]`), but `typing.get_args()` on a lazy `TypeAliasType` returns `()`. Every `_NAMES` list is therefore empty, so any `__init__` call dies in `normalize_str` (ints → `IndexError`, names → `ValueError`).

Because subclassing with `_NAMES`/`_MIN`/`_MAX` is the documented extension API of the base classes, the standard tests exercise all of the (otherwise unreachable) Month/Weekday/Season/Hour logic through minimal `Fixed*` subclasses (`tests/helpers.py`) that re-supply **only** the broken `_NAMES` attribute. `Month.nth_weekday` hardcodes the shipped `Weekday` class internally, so those tests additionally patch `Weekday._NAMES`/`_LOOKUP` via `pytest-mock` — the minimum intervention required.

---

## Rejected behaviors (defect register)

Behavior below is **not** covered by standard tests and is **excluded from the coverage goal**. Each defect is pinned by tests in `tests/test_reject_verification.py` (marked `reject_verification`), which should be deleted once fixed. Coverage evaluation includes these tests, which is how the defective lines still reach 100%.

### D1 — Named components are unconstructible
* **Where:** `month.py:17`, `weekday.py:15`, `season.py:10`, `hour.py:18`
* **What:** `_NAMES = list(get_args(<PEP 695 alias>))` evaluates to `[]`; all construction fails (see above).
* **Trivial repair:** use the alias's value, e.g. `list(get_args(MonthName.__value__))`, or spell the lists out literally.

### D2 — `size()` is off by one, corrupting all wrap-around arithmetic
* **Where:** `base.py:46` (`return cls._MAX - cls._MIN`), poisoning `__add__`/`__sub__` (`base.py:78–98`).
* **What:** an inclusive range has `_MAX - _MIN + 1` values. `Minute.size()` reports 59, `Weekday.size()` 6. Consequences: `Weekday(6) + 1` → *tuesday* (should be *monday*); `Month(12) + 1` → *february*; `Month(1) - 1` → *november*; and even the **in-range** shift `Minute(50) + 9` returns `0` instead of `59`, because landing exactly on `_MAX` falsely triggers a wrap.
* **Trivial repair:** `return cls._MAX - cls._MIN + 1`.
* Standard tests only assert non-wrapping shifts that stay strictly below `_MAX`, where behavior is correct.

### D3 — `Month.monthrange()` February guard is inverted
* **Where:** `month.py:42–43` — `if self.int_id == 2 and self.has_year(): raise ...`
* **What:** the docstring says the year is *required* for February, but the code raises exactly when the year **is** set (`len(Month(2, 2024))` → `ValueError`) and silently answers 28 (1970) when it isn't. This also breaks `nth_weekday`/`__len__` for any February with a year.
* **Trivial repair:** `if self.int_id == 2 and not self.has_year(): raise ...`

### D4 — `__add__` drops the year; the `_apply_loop` year bump is dead code
* **Where:** `base.py:87` (`result = type(self)(wrapped_int)`) vs. `month.py:98–104` and `season.py:28–34`.
* **What:** the base rebuilds the result without the `year` argument, so `Month(5, 2024) + 1` has `year=None`, and the year-adjusting `_apply_loop` overrides can never see a year — `Month(12, 2024) + 1` should be January 2025 but has no year at all. `create_from(instance)` (`base.py:41`) drops the year the same way, so the "copy" doesn't even compare equal to its source under the year-aware `__eq__`.
* **Trivial repair:** have `Month`/`Season` override `__add__` to re-attach `self.year` (or have the base use a copy hook instead of bare `type(self)(int)`).

### D5 — `Month.last_nth_weekday` can never succeed
* **Where:** `month.py:72–96` (everything after the year guard; `month.py:88` builds `self + 1`).
* **What:** direct consequence of D4 — the internally built next month has no year, so the nested `nth_weekday` call raises `"Year must be set"` for *every* valid input. Lines 88–96 are unreachable through any public path. The reject tests prove (via a year-propagating subclass) that the remaining logic is otherwise sound — last Friday of May 2024 = 31 — so fixing D4 fixes this for free.

### D6 — `Duration.total_seconds()` uses 8 640 seconds per day
* **Where:** `duration.py:52` (`+ s.days * 8640`).
* **What:** a day is 86 400 seconds; the factor is 10× too small. Because `simplify()` converts day multiples of 7 into (correct) weeks, the error surfaces only for day remainders — `Duration(days=1).total_seconds()` → 8 640; `Duration(days=1) < timedelta(hours=3)` → `True`. Everything routed through `total_seconds` (comparisons, `/` by durations, `to_timedelta`, `abs`, `bool`) inherits this for day-bearing values.
* **Trivial repair:** `86400`.
* Standard tests only assert totals whose simplified form is day-free (sub-day amounts or exact week multiples), where behavior is correct.

### D7 — `simplify()` corrupts negative fractional seconds
* **Where:** `duration.py:104` (`total_minutes += int(total_seconds) // 60`).
* **What:** `int()` truncates toward zero while `%` floors, so `Duration(seconds=-0.5).simplify()` becomes **+59.5 s** with no compensating −1 minute — the duration changes value. Negative *integer* seconds borrow correctly by contrast.
* **Trivial repair:** `math.floor(total_seconds) // 60` (matching the downward-cascade code a few lines above).

### D8 — `__neg__` needlessly demands exactness and collapses structure
* **Where:** `duration.py:182–183` (`return Duration.create_from(-self.total_seconds())`).
* **What:** negating is representable field-by-field, yet the implementation round-trips through `total_seconds`, so `-Duration(months=1)` raises `ValueError` and `Duration(months=3) - Duration(months=1)` is impossible (`__sub__` negates its operand). Combined with D6, `abs(Duration(seconds=-5))` returns a duration of **77 765 s**. `__abs__`'s negative branch (`duration.py:225`) is only reachable through this defective path.
* **Trivial repair:** `return self * -1`-style field negation (e.g. construct with each field negated, preserving `month_days`/`year_days`).

### Excluded-from-goal lines (only covered by reject tests)
`base.py` 76, 89 · `month.py` 43, 82–96, 102–104 · `season.py` 32–34 · `duration.py` 225. All other lines/branches are covered by the standard suite.

---

## What was tested (standard suite)

All tests follow the standard architecture: one `...MixinBase` (condition + abstract fixtures) per feature, a positive `...Mixin` and a negated `No...Mixin` holding the `test_` methods (each a single `assert self.validate(...)`), group mixins, and concrete `Test*` classes that implement fixtures only. Exception features use the `Fails...` naming with `fail_<feature>` set; per the `validate` contract those are consumed through their `No...` variant so the assertion passes.

| File | Features (marks) |
|---|---|
| `tests/test_base.py` | Full plain + named contract pinned against minimal local subclasses (`Dozen`, `Coin` with an alias) — the documented subclassing API of `base.py`, independent of the shipped components. |
| `tests/test_minute.py` / `test_second.py` | Plain numeric contract: int construction & `__int__`, documented clamping (ctor + `int_id` setter), bool rejection, string rejection, `int_id` equality/hash, `create_from` copying, `argtype` parsing & junk rejection, non-wrapping `+`/`-` immutability. `TestSecond(TestMinute)` inherits everything unchanged. |
| `tests/test_weekday.py` | Inherits the whole numeric suite from `TestMinute` **with `negative_rejects_string_values = True`** (named components legitimately accept names — the inherited test flips to verify the override), plus naming contract and `datetime.date.weekday()` parity (Monday = 0). |
| `tests/test_hour.py` | Numeric + naming contracts, `midnight`/`noon` alias resolution, `to_24h`/`to_12h` conversions. |
| `tests/test_season.py` | Numeric + naming contracts, `fall`→`autumn` alias, optional-year tracking, year-aware equality/hash. |
| `tests/test_month.py` | Numeric + naming + year contracts; `monthrange`/`len` vs. stdlib `calendar` (non-February), `nth_weekday` from names/ints/instances with `n<1` clamping and beyond-month rejection (with `Weekday` name table patched per D1), and the up-front year guards of both weekday-math methods (method-focused test classes). |
| `tests/test_duration.py` | Construction (`from_seconds`, `from_timedelta`, `create_from` incl. passthrough & `TypeError`), simplification (fraction cascade, upward carry, week rollup, `year_days`/`month_days` folding), `is_simplified` + idempotent `simplify` (cache), day-free `total_seconds`/`to_timedelta`, inexact-unit guards (weekdays/months/years as separate method-focused classes), `+ - * /` with Durations/numbers/timedeltas from both sides, duration-ratio division, sign ops on exact values, `NotImplemented`→`TypeError` for every operator, value equality/hash across unit mixes, ordering, truthiness. |
| `tests/test___init__.py` | Package re-exports of all component classes. |

Naming/normalization behaviors verified include case-insensitivity, canonical `str()`, `str_id`/`int_id` setter synchronization, class-level `normalize_int`/`normalize_str`/`argtype`/`create_from` (all marked `static`), alias filtering in `__init_subclass__`, and `ValueError`/`TypeError` guards.

## How your requirements were met

* **Coverage:** 100% line **and** branch coverage on every source file (see table above), with reject-verification tests supplying the defective regions, which are explicitly excluded from the goal per policy.
* **Marks by feature:** every test carries one or more `feature_*` marks (registered in `pytest.ini`, `--strict-markers` enforced) — e.g. `-m feature_aliases` selects exactly the alias tests.
* **Static marks:** every test exercising a class-level/static method (`normalize_int`, `normalize_str`, `argtype`, `create_from`, `from_seconds`, `from_timedelta`) is marked `static` (52 tests).
* **General utility:** behavior is pinned at the *contract* level (base-class suites re-run against every component and against minimal local subclasses), so other projects adopting any subset get the same guarantees.
* **Python 3.12+:** the suite runs on 3.12; ironically that very requirement is what exposes D1.

## Suggested features (tests included, `suggested_feature` + `xfail`)

In `tests/test_suggested_components.py` / `tests/test_suggested_duration.py` — all currently xfail and flip to passing once implemented:

* **S1** Export `duration` from the package root (`__init__.py` is missing `from .duration import *` — today `dateutils.Duration` doesn't exist).
* **S2** `Weekday.from_date(d)` / `Month.from_date(d)` (year-carrying) for stdlib interop.
* **S3** `Season.for_month(month)` meteorological mapping.
* **S4** `Hour.is_am()` / `Hour.is_pm()` predicates.
* **S5** Rich ordering (`<`, `<=`, …) on components so they sort naturally.
* **S6** `Duration.total_minutes()/total_hours()/total_days()`.
* **S7** `Duration.from_iso8601("PT1H30M")` parsing for API-facing services.

## Tests refused, and why

No standard tests were written asserting the following as correct — they are the defects above, and baking them into the expected-behavior suite would cement wrong behavior:

1. Instantiating the shipped `Month`/`Weekday`/`Season`/`Hour` (D1 — impossible).
2. `size()` return values and any wrap-around `+`/`-` results, including shifts landing exactly on `_MAX` (D2).
3. `monthrange`/`len`/`nth_weekday` on February (D3).
4. Year propagation through `+`/`-`/`create_from` on `Month`/`Season` (D4).
5. `last_nth_weekday` beyond its year guard (D5 — cannot succeed).
6. `total_seconds` (and anything routed through it) for durations whose simplified form contains loose days (D6).
7. `simplify()` of negative fractional seconds (D7).
8. `__neg__`/`__sub__` involving months/years/weekdays, and `abs()` of negative durations (D8).

Each is instead pinned by a `reject_verification` test so the defect's presence is machine-checked until fixed.

### Additional notes (not rejections)

* Silent clamping of out-of-range ints (`base.py` `normalize_int`) is unusual but explicitly documented, so it is tested as expected behavior; consider whether callers would prefer a `ValueError`.
* `__mul__`/`__truediv__` call `_assert_exact`, so `Duration(months=1) * 2` raises even though scaling months is representable — a deliberate-looking restriction worth revisiting alongside D8.
* `weekday.py` imports `cast` unused; harmless.
