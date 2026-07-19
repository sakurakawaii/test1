# Northbridge Mutual — FY2025 Capital Close Note (Board Pack Freeze, 16 January 2026)

**Sources:** close folder only (locked CAP_R4 totals, CAP_R4 driver detail, Finance v5 and Risk v6 signed single-function bases, FY2024 signed board note, support schedules, late-item log, approval notes). No external sources used.

---

## 1. Bottom line

**The pack can be sent.** There is no fatal issue. The Finance v5 table is usable as the working board view, exactly as the Finance Director's pack-freeze instruction allows, provided three things hold:

1. **Totals are presented as final; the module split is not.** Eligible own funds, total SCR, MCR and both coverage ratios come straight from locked CAP_R4 and are final. The risk-module attribution is a **working view only** — the required combined Finance Control + Capital Risk approval (`CAP_ATTRIB_Q4_COMBINED_APPROVAL_v7.pdf`) has not arrived, so control rule 3 applies: it must not be described as final module-level attribution. `capital_board_table.csv` labels every row accordingly.
2. **The Risk v6 alternative is shown, because it genuinely changes the story** (section 3 below).
3. **Four pieces of draft wording are removed** — dividend capacity, "capital target achieved", "no solvency concerns", and the bonus scorecard conclusion are all unsigned and must not go to the Board as conclusions (section 5 below).

## 2. The capital position — FINAL (locked CAP_R4)

| Metric | FY2025 | FY2024 signed | Movement | Status |
|---|---|---|---|---|
| Eligible own funds | GBP 642.0m | GBP 615.0m | +27.0m | Final — locked |
| Total SCR | GBP 455.0m | GBP 438.0m | +17.0m | Final — locked |
| MCR | GBP 168.0m | GBP 164.0m | +4.0m | Final — locked |
| SCR coverage | 141.10% | 140.41% | +0.69 pts | Final — locked |
| MCR coverage | 382.14% | 375.00% | +7.14 pts | Final — locked |

All figures verified arithmetically: the ten CAP_R4 drivers sum to 455.0, Tier 1 (512.0) + Tier 2 (130.0) = 642.0, and both ratios recompute exactly. Own funds are after elimination of the intercompany capital-support recharge, which is kept entirely out of the external position and out of movement commentary. The management candidate table omitted the MCR and MCR coverage rows required by the table instructions; they have been added from CAP_R4.

## 3. Risk-module attribution — WORKING VIEW (Finance v5), with Risk v6 alternative

Both views are signed by one function only, and **both reconcile exactly to the locked SCR of GBP 455.0m** — only the split differs. The disagreement is GBP 24.0m of presentation across three items (C503 GBP 20.0m, C509/C510 GBP 4.0m), but it **changes the movement story**, so it is shown:

| Module | Finance v5 (move vs FY2024) | Risk v6 (move vs FY2024) | Difference |
|---|---|---|---|
| Insurance underwriting | 192.0 (+8.0) | 172.0 (−12.0) | −20.0 (C503 hedge overlay) |
| Market | 138.0 (+9.0) | 158.0 (+29.0) | +20.0 (C503 hedge overlay) |
| Counterparty credit | 34.0 (−15.0) | 34.0 (−15.0) | nil — agreed |
| Operational | 38.0 (+2.0) | 42.0 (+6.0) | +4.0 (model governance overlay) |
| Other / diversification | 53.0 (+13.0) | 49.0 (+9.0) | −4.0 (same overlay, netted) |
| **Total SCR** | **455.0 (+17.0)** | **455.0 (+17.0)** | **nil** |

**Why this matters to the Board:** on Finance v5 the SCR increase looks broad-based, with underwriting capital *rising* GBP 8.0m. On Risk v6, underwriting capital *falls* GBP 12.0m and Market is by far the dominant driver (+GBP 29.0m, and 34.7% of SCR vs 30.3%). Which narrative the Board hears depends on an unresolved classification call on the GBP 20.0m longevity hedge overlay (underwriting origin vs market/collateral stress driver). The total position, coverage ratios and the counterparty improvement (−15.0m) are identical under both views.

## 4. Late and cut-off items — all handled per control rules, none adjust the table

- **LC01 — January asset de-risking trade, GBP 12.0m (5 Jan):** excluded from the 31 Dec position. A post-year-end management action; may be disclosed as an events-after note only, kept separate from the locked table.
- **LC02 — Subordinated debt coupon true-up, GBP 3.0m:** already inside CAP_R4 own funds; **not** double counted.
- **LC03 — January model recalibration, GBP 9.0m (8 Jan):** excluded; post-year-end and unsigned.
- **LC04 — Intercompany capital-support recharge, GBP 6.0m:** eliminated to nil; not external capital and excluded from all movement commentary.

## 5. Is the capital-target / bonus / dividend wording safe? **No — not yet.**

The draft board commentary contains four conclusions that the control rules (rule 8) and the approval evidence do not support. Each is kept separate and each fails for its own reason:

| Draft wording | Safe? | Why not |
|---|---|---|
| "No dividend-capacity concerns" | **No** | `Treasury_Capital_Distribution_FY2025_signed.pdf` not filed; Treasury says not yet signed |
| "Capital target achieved" / "above the 140% target" as a conclusion | **No** | Board Risk Committee has not signed the FY2025 capital target note; the Q3 note may not be quoted |
| "No solvency concerns" | **No** | "No concerns" wording requires the relevant signed FY2025 review |
| "Bonus scorecard condition satisfied" | **No** | RemCo support not signed; it also depends on the final attribution and dividend review |

**What *can* be said safely:** SCR coverage of 141.10% and MCR coverage of 382.14% are locked facts, and the 1.40 policy target (with a 1.45 risk-appetite upper zone) may be shown as **context**. The arithmetic comparison is visible to the Board without management asserting achievement, distribution capacity, or bonus outcomes. Also not safe: the draft's claim that "the Finance v5 table is ready for board approval" — it is a working view pending combined approval.

## 6. What still needs fixing (owners)

1. **Chase `CAP_ATTRIB_Q4_COMBINED_APPROVAL_v7.pdf`** (Finance Control + Capital Risk) — resolves C503, the C509/C510 overlay, and the C510 presentation, and lets the module split be called final. Until then, attribution stays labelled "working view".
2. **Treasury** to file the signed FY2025 capital-distribution review before any dividend-capacity wording is used.
3. **Board Risk Committee** to sign the FY2025 capital target note before any "target achieved" conclusion.
4. **RemCo support** to sign the scorecard conclusion before any bonus wording.
5. **Finance** to correct the candidate table at source: replace module "Ready" flags with working-view labels and add the MCR rows.

## 7. Outputs in this pack

- `capital_board_table.csv` — board table: Section A final locked position, Section B Finance v5 working attribution with Risk v6 alternative columns, Section C wording status (clearly separated from the figures).
- `capital_attribution_exceptions.csv` — 13 exceptions with amounts, both treatments, today's pack treatment, and owners.
- `capital_close_note.md` — this note.

*Prepared from the close folder only. Figures in GBP millions. Nothing in this note constitutes a signed dividend-capacity, capital-target, solvency, or bonus conclusion.*
