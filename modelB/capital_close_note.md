# Northbridge Mutual — FY2025 Capital Close Note (Board Pack Freeze, 16 Jan 2026)

## 1. Verdict

**The Finance v5 table is usable as today's working board view. There is no fatal issue with the numbers.**
All totals and coverage ratios tie exactly to locked CAP_R4, the FY2024 comparatives tie to the signed
prior-year note, every arithmetic check passes, and all four late/cutoff items are correctly excluded.

What is **not** final is (a) the split of SCR between risk modules, because the required combined
Finance Control + Capital Risk approval (`CAP_ATTRIB_Q4_COMBINED_APPROVAL_v7.pdf`) has not arrived,
and (b) the conclusion wording — none of the capital-target / dividend / bonus sign-offs are in the folder.
`capital_board_table.csv` labels each row accordingly.

| Element | Status |
|---|---|
| Eligible own funds £642.0m (+£27.0m) | **FINAL — locked CAP_R4** |
| Total SCR £455.0m (+£17.0m) | **FINAL — locked CAP_R4** |
| MCR £168.0m (+£4.0m) | **FINAL — locked CAP_R4** |
| SCR coverage 141.10% (PY 140.41%) | **FINAL — locked**; identical under v5 and v6 |
| MCR coverage 382.14% (PY 375.00%) | **FINAL — locked** |
| Module attribution (5 rows) | **WORKING VIEW — NOT FINAL** (combined approval pending) |
| Dividend / target / solvency / bonus wording | **NOT SAFE** — see section 4 |

## 2. Board table basis

Per the pack-freeze instruction, the table uses **Finance v5** (signed by Finance only, 12 Jan) as the
working attribution, with the **Risk v6** alternative (signed by Risk only, 13 Jan) shown alongside
because it changes the story (section 3). Both views sum to the locked £455.0m SCR, so the dispute is
presentational — it cannot move own funds, total SCR, MCR, or either coverage ratio.

## 3. Does the Risk v6 alternative change the story? Yes — for the movement narrative

Two reclassifications, £24.0m of presentation swing in total:

| Module | v5 (working) | v6 (alt) | Movement vs FY2024: v5 | v6 |
|---|---:|---:|---:|---:|
| Insurance underwriting | 192.0 | 172.0 | **+8.0** | **−12.0** |
| Market | 138.0 | 158.0 | **+9.0** | **+29.0** |
| Counterparty credit | 34.0 | 34.0 | −15.0 | −15.0 |
| Operational | 38.0 | 42.0 | +2.0 | +6.0 |
| Other / diversification | 53.0 | 49.0 | +13.0 | +9.0 |
| **Total SCR** | **455.0** | **455.0** | **+17.0** | **+17.0** |

- **C503 longevity hedge overlay, £20.0m** — v5: Underwriting (origin of exposure); v6: Market
  (the year's increase comes from market basis/collateral stress). This single item determines whether
  the board is told underwriting capital **rose £8m** or **fell £12m**, and whether market risk rose
  **£9m** or drove **almost the entire £17m SCR increase (+£29m)**.
- **Model governance overlay, £4.0m** — v6 shows it in Operational (38→42); v5 leaves it in
  Other/diversification (53 vs 49). Smaller, but affects the operational-risk trend line.
- v5 and v6 **agree** on Counterparty credit (−£15.0m is solid either way).

**Recommendation:** present v5 as the working view with the v6 column visible, and do not let the
narrative lean on "underwriting-driven" vs "market-driven" until the combined approval lands.

## 4. Is the wording safe? No — four separate verdicts

Control rule 8 bars final conclusion wording without the signed FY2025 review. All four sign-off files
are listed as *expected but not received*. Each item below is a separate gate — do not combine them.

1. **Dividend capacity — NOT safe.** `Treasury_Capital_Distribution_FY2025_signed.pdf` not filed;
   Treasury confirms not yet signed. Remove "no dividend-capacity concerns" from the draft commentary.
2. **Capital target — NOT safe as a conclusion.** BRC has not signed the FY2025 capital target note and
   the Q3 note may not be quoted. The *fact* that 141.10% exceeds the 140% policy threshold may be stated,
   labelled as a policy comparison — note the headroom above 1.40× is only ~£5.0m / 1.1 pts, and the
   position sits below the 1.45× upper risk-appetite zone, so the conclusion genuinely belongs to BRC.
3. **Solvency conclusion — NOT safe.** "Capital position is therefore adequate, with no solvency
   concerns" is a "no concerns" statement with no signed review behind it. Also, the draft's claim that
   "the Finance v5 table is ready for board approval" is wrong — v5 is a single-function working view.
4. **Bonus — NOT safe.** RemCo support has not signed the scorecard conclusion; it depends on the final
   attribution and the dividend review. Delete the bonus sentence entirely.

**Safe replacement wording for the pack:**

> FY2025 eligible own funds were £642.0m and total SCR was £455.0m (both locked, CAP_R4), giving SCR
> coverage of 141.10% (FY2024: 140.41%) and MCR coverage of 382.14% (FY2024: 375.00%). SCR coverage is
> arithmetically above the 140% capital-policy threshold; the FY2025 capital target, dividend-capacity
> and bonus-scorecard conclusions remain subject to the outstanding Board Risk Committee, Treasury and
> RemCo reviews and are not concluded in this pack. The risk-module attribution is shown on the Finance
> v5 working basis pending combined Finance/Risk approval; the Capital Risk alternative reallocates
> £20.0m (longevity hedge overlay) from Insurance underwriting to Market and £4.0m (model governance
> overlay) from Other/diversification to Operational, with no effect on total SCR or coverage.

## 5. Main issues still to fix (before the final pack)

1. **Obtain `CAP_ATTRIB_Q4_COMBINED_APPROVAL_v7.pdf`** and settle C503 (£20.0m), the £4.0m overlay, and
   the C510 allocation presentation. Until then the five module rows stay "working view". (EX-01/02/03/05)
2. **Clear the residual dispute flags on C507/C508** in the locked detail — both functions already agree
   they are Counterparty credit, so this looks like a stale flag to confirm at sign-off. (EX-04)
3. **Recut the draft board commentary** (file 15) using the safe wording above; chase the Treasury, BRC
   and RemCo sign-offs for the conclusions. (EX-10/11/12/13)
4. **Hold the cutoff line in commentary**: the January de-risking trade (£12.0m), January recalibration
   (£9.0m) and the January intercompany recharge (£6.0m) are correctly out of the 31 Dec position and
   must not creep into the movement narrative; the £3.0m sub-debt coupon true-up is already in CAP_R4
   and must not be added again. (EX-06–09)

## 6. Checks performed (all from folder files only)

- Driver detail (05) sums to £455.0m = CAP_R4 SCR; v5 (06) and v6 (07) each sum to £455.0m. ✓
- Management candidate table (09) re-derived from drivers: every amount, movement and % of SCR correct;
  its "Ready/Final" flags were **overridden** for module rows (not final without combined approval). ✓
- Tier 1 £512.0m + Tier 2 £130.0m = £642.0m own funds; intercompany recharge eliminated to nil. ✓
- Coverage ratios recomputed: 642/455 = 141.10%; 642/168 = 382.14%; PY 615/438 = 140.41%, 615/164 = 375.00%. ✓
- All four cutoff-log items (13) verified as correctly excluded / not double counted in both views. ✓

*Prepared from the FY2025 close folder only. Totals are locked; module attribution and all conclusion
wording are labelled not final as above.*
