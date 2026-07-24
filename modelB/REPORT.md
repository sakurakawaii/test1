# Test Report: `datecomponents` date utility

## Summary

| | |
|---|---|
| Tests written | **260** (252 passing, 8 `xfail` for suggested features) |
| Standard feature tests | 230, organized as `Mixin` features per the Bedrock utility suite |
| Reject-verification tests | 22 (marked `reject_verification`, proving the defects below) |
| Suggested-feature tests | 8 (marked `suggested_feature`, `xfail(strict=True)`) |
| Raw coverage (line + branch, incl. reject tests) | 94% line / 88 branches, 2 partial |
| Coverage of **non-rejected** code | **100% line and 100% branch** — every missed line/branch sits inside a rejected section (itemized below) |

Run with:

```bash
pip install pytest pytest-cov
pytest --cov=datecomponents --cov-branch --cov-report=term-missing
pytest -m "not reject_verification"   # hide defect proofs
pytest -m static                      # only classmethod/static-level tests
```

> The sources were copied unmodified into `datecomponents/`. No repairs were
> performed, per policy; trivial fixes are suggested inline below.

---

## 🔴 Rejected behavior (defects)

These behaviors would not be reasonably expected by any user. **No standard
tests assert them**; instead each is *proven present* by a test in
`tests/test_rejections.py`, and the code they make unreachable is excluded
from the coverage goal.

### D1 — All named components are unusable on Python 3.12+ (critical)
* **Where:** `weekday.py:15`, `month.py:17`, `season.py:10`, `hour.py:18`
* **What:** `typing.get_args()` returns `()` when applied to a PEP 695
  `type` alias (it does not unwrap `TypeAliasType`), so `_NAMES` is an empty
  list for `Month`, `Weekday`, `Season` and `Hour`. Consequently **no shipped
  named component can be constructed at all**: int input crashes with
  `IndexError` from `normalize_str`, and every valid name (e.g. `"may"`,
  `"monday"`, `"noon"`) is rejected with `ValueError`.
* **Trivial repair:** use `list(get_args(MonthName.__value__))` (etc.), or
  declare the aliases as plain assignments (`MonthName = Literal[...]`).
* **Proof:** `TestD1NamedClassesAreUnusable`.
* **Testing workaround:** each test file defines a `Usable<Component>`
  subclass that supplies the intended `_NAMES` via the *documented* extension
  contract ("Subclasses must define `_NAMES`, `_MIN`, and `_MAX`"), so the
  components' own logic is still fully verified.

### D2a — `size()` is off by one, breaking all wrap-around arithmetic
* **Where:** `base.py:46` (`return cls._MAX - cls._MIN`), consumed by
  `__add__`/`__sub__` at `base.py:83-85`.
* **What:** for inclusive bounds the count is `_MAX - _MIN + 1`. As shipped,
  `Minute.size() == 59` (should be 60), so *every* wrap is wrong —
  `Minute(59) + 1 == Minute(1)` (should be 0) — and even additions landing
  exactly on `_MAX` spuriously wrap: `Minute(50) + 9 == Minute(0)` (should
  be 59).
* **Trivial repair:** `return cls._MAX - cls._MIN + 1`.
* **Proof:** `TestD2SizeOffByOneBreaksWrapAround`.
* **Standard tests** therefore only assert additions/subtractions that stay
  strictly below `_MAX` (landing on `_MIN` is safe).

### D2b — `__add__` silently drops the `year` of Month/Season
* **Where:** `base.py:87` (`result = type(self)(wrapped_int)`), defeating
  `month.py:102-103` and `season.py:32-33`.
* **What:** the new instance is built without forwarding the year, so
  `Month(3, 2024) + 1` has `year is None`, and the `_apply_loop` year
  adjustment (`self.year += loop_count`) can never execute — **dead code**.
  This also makes `last_nth_weekday` unusable for *every* month, because its
  `self + 1` shortcut produces a year-less month that trips the inner
  `nth_weekday` year guard (`month.py:88-89`).
* **Trivial repair:** give `__add__` a copy hook (e.g. construct via a
  `_replace_int(wrapped_int)` method subclasses override to carry state).
* **Proof:** `TestD2YearLostOnArithmetic`,
  `TestD4WeekdayHelpersUnreachable::test_last_nth_weekday_always_raises_for_yeared_months`.

### D3 — `monthrange()` February condition is inverted
* **Where:** `month.py:42-43` (`if self.int_id == 2 and self.has_year():`)
* **What:** the docstring promises the opposite: February **with** a year
  raises `ValueError("Year must be set…")`, while February **without** a year
  silently uses 1970 (always 28 days). `len(Month("february", 2024))` is
  therefore impossible.
* **Trivial repair:** `if self.int_id == 2 and not self.has_year():`.
* **Proof:** `TestD3MonthrangeFebruaryConditionInverted`.

### D4 — `nth_weekday` / `last_nth_weekday` unreachable beyond their guards
* **Where:** `month.py:57` and `month.py:82` (`Weekday.create_from(...)`),
  making `month.py:59-70` and `month.py:84-96` dead code.
* **What:** consequence of D1 (+D2b for `last_nth_weekday`): the internal
  `Weekday` construction always raises, so only the "year must be set" guard
  clauses are live. The guards themselves are covered by standard tests
  (`FailsNthWeekdayWithoutYearMixin`); everything after line 57/82 is
  excluded from the coverage goal.
* **Proof:** `TestD4WeekdayHelpersUnreachable`.
* *Note:* once D1/D2b are fixed, the formula at `month.py:64` looked correct
  in manual walkthroughs (e.g. 2nd Monday of March 2024 → 11) — add standard
  tests then.

### D5 — Days convert at 8640 seconds instead of 86400
* **Where:** `duration.py:52` (`+ s.days * 8640`)
* **What:** a missing zero: `Duration(days=1).total_seconds() == 8640`. Since
  `simplify()` folds whole weeks out first, only spans whose simplified form
  has a non-zero day remainder are corrupted (e.g. `Duration(hours=25)` →
  12 240 s instead of 90 000 s). Negative spans that borrow through the days
  place (e.g. `abs(Duration(seconds=-90))`) are corrupted too.
* **Trivial repair:** `+ s.days * 86400`.
* **Proof:** `TestD5DaysConvertAt8640Seconds`.
* **Standard tests** assert totals only via seconds/minutes/hours(<24)/weeks
  and via pinned lengths that are whole weeks (28/364 days).

### Minor defects
* **M1** — `__init__.py` never imports `duration`, so `Duration` is missing
  from the package namespace. Repair: add `from .duration import *`.
  Proof: `TestM1DurationNotExported`.
* **M2** — `create_from` (`base.py:37-41`) quietly accepts `bool` via
  `cls(int(value))`, bypassing the constructor's deliberate bool guard
  (`base.py:54`). Repair: move the guard into `create_from` or check
  `isinstance(value, cls)` for the copy path. Proof:
  `TestM2CreateFromBoolInconsistency`.

### Design concerns (reported only, current behavior *is* tested)
* **C1** — out-of-range ints clamp silently (documented, tested as-is), which
  can mask caller bugs; consider a strict mode.
* **C2** — `Duration.__eq__`/`__hash__` treat `month_days`/`year_days` as part
  of identity, so `Duration(years=1, year_days=364) + Duration(weeks=1)` is
  **not** `== Duration(weeks=53)` despite identical spans. Tests compare
  structure/totals instead.
* **C3** — `Duration.__mul__`/`__truediv__`/`__bool__`/`__neg__` raise
  `ValueError` for month/year/weekday-bearing durations even where the result
  is well-defined (e.g. `Duration(months=1) * 2`); note that `bool()` raising
  is particularly surprising in `if duration:` contexts. Current behavior is
  pinned by `FailsScalingInexactUnitsMixin` / `FailsTotalWithInexactUnitsMixin`.

---

## Coverage accounting

Raw run (standard + reject + suggested tests): **94% line**, 2 partial
branches. Every miss is inside a rejected section:

| Missed | Rejected by |
|---|---|
| `month.py` 59-70 | D4 (dead after `Weekday.create_from` raise) |
| `month.py` 84-96 | D4/D2b (dead after `Weekday.create_from` raise) |
| `month.py` 103 + partial branch 102→103 | D2b (year is always `None` in `_apply_loop`) |
| `season.py` 33 + partial branch 32→33 | D2b (same) |

Excluding those rejected lines/branches, coverage of in-scope code is
**100% line and 100% branch** across all nine source files (`base.py`,
`duration.py`, `hour.py`, `minute.py`, `month.py`, `season.py`, `second.py`,
`weekday.py`, `__init__.py`). No `# pragma` edits were made to the sources.

---

## Suite architecture & requirement mapping

* `tests/test_utils.py` — the standard Bedrock `Mixin` utility (verbatim).
* Every behavior is a **feature** implemented as an abstract trio:
  `<Feature>MixinBase` (implements `condition`, declares fixtures),
  `<Feature>Mixin` (`negative_<feature> = False`, holds the `test_` methods,
  which only call `self.validate`), and `No<Feature>Mixin` (extends the
  positive mixin, flipping `negative_<feature> = True` so it inherits the
  same tests negated). Exception-checking bases are named `Fails…` and set
  `fail_<feature>`; their tests are bare `validate` calls because the
  `pytest.raises` inside `validate` is the assertion. Feature names are the
  snake_case of the base-class name minus `MixinBase`.
* Shared features live in `tests/mixins/` (`numeric.py`, `named.py`,
  `yeared.py`); `PlainNumericComponentMixin` / `NamedComponentMixin` are the
  empty abstract grouping classes. Duration- and Month-specific features sit
  above their test classes in the same file.
* **Fixtures are implemented only in the lowest-level test classes**; the
  mixin bases declare them unimplemented.
* **Subclass inheritance with negation** (per guidelines):
  `TestSecond(TestMinute)` re-runs the whole suite against `Second`;
  `TestMonthWithoutYear(TestMonthWithYear)` and
  `TestSeasonWithoutYear(TestSeasonWithYear)` flip `negative_has_year`,
  `negative_year_or_default_returns_own_year` and un-flip
  `negative_year_default_is_1970`; `TestDurationUnequalSpans`,
  `TestWeekdayIsWeekendMidweek`, `TestHourMeridiemAfternoon` use the same
  mechanism.
* **Marks (your request):** feature-category marks `construction`,
  `normalization`, `identity`, `arithmetic`, `calendar`, `conversion`,
  `comparison`, `simplification`, `argparse_support` are applied on every
  test method; every test exercising a classmethod/static-level API
  (`create_from`, `normalize_int`, `normalize_str`, `argtype`,
  `from_seconds`, `from_timedelta`, …) additionally carries
  `@pytest.mark.static` (68 tests). All marks are registered in `pytest.ini`.
* One test file per source file: `test_base.py`, `test_month.py`,
  `test_weekday.py`, `test_season.py`, `test_hour.py`, `test_minute.py`,
  `test_second.py`, `test_duration.py` (+ `test_rejections.py`,
  `test_suggested_features.py`). `__init__.py` is covered by importing the
  package. No `conftest.py`, no `parametrize`, no mocking, plain `assert`s
  only; all tests are deterministic (fixed dates/years) and order-independent.

### Behavior verified (highlights)
* **base / all components:** in-range construction, silent clamping, bool/
  float rejection, `int_id` setter re-normalization, equality & hash
  contracts, cross-type inequality (`No…` variants), `int()` conversion,
  non-wrapping `+`/`-` returning new instances, `create_from` (int / copy /
  name), `normalize_int`, `normalize_str` (int & name & unknown-name &
  bad-type), `argtype` (numeric string, name fallback, invalid input).
* **named components:** case-insensitive names, canonical `str()`/`str_id`,
  synchronized int/str setters, alias resolution (`fall`→`autumn`,
  `noon`→`12pm`, case-insensitive).
* **Month/Season:** `has_year`, `year_or_default` (both branches via the
  with/without-year class pair), year-sensitive equality & hash,
  `monthrange`/`len` for real and 1970-default years, the year guards of
  `nth_weekday`/`last_nth_weekday`.
* **Hour:** `to_24h`/`to_12h`.
* **Duration:** zero default, `from_seconds`/`from_timedelta`/`create_from`
  (all dispatch paths + `TypeError`), `total_seconds`/`to_timedelta` on
  exact units, refusal of weekday/month/year totals, `month_days`/`year_days`
  pinning (incl. preservation through `+` from either operand), `simplify`
  (upward normalization, fractional cascade, idempotence/cache,
  `is_simplified`), equality across unit spellings + hash, full operator
  surface (`+ - * / // abs pos neg bool < <= > >=`) with both Duration /
  `timedelta` / numeric operands and `TypeError` for foreign operands
  (10 separate guard tests).

---

## Suggested features (tests in `tests/test_suggested_features.py`, all `xfail(strict=True)`)

| # | Suggestion | Rationale |
|---|---|---|
| S1 | `Weekday.is_weekend()` (and implicitly `is_workday()`) | extremely common scheduling predicate |
| S2 | `Weekday.from_date(datetime.date)` classmethod | the class already promises `datetime.date.weekday()` parity |
| S3 | `Month.season()` ↔ `Season.months()` | bridges the two components the package already ships |
| S4 | `Hour.is_am()` / `Hour.is_pm()` | complements `to_12h()`/`to_24h()` |
| S5 | `Duration.total_days()` | symmetric with `total_seconds()`, mirrors `timedelta` ergonomics |
| S6 | `Duration.__floordiv__` (Duration/timedelta) | "how many whole spans fit" — natural next to the existing `/` ratio |

Each has a working-condition test that will flip to a loud `XPASS(strict)`
the moment the feature lands, reminding you to promote it into the standard
suite.
