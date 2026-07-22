# Internal decision memo — AI camera inspection pilot (final-pack lines)

**Subject:** Wider rollout funding request and June spend position
**Basis:** W22/W23 review pack, source extracts to 3 June 2025 (camera, MES, QPulse, service, finance v3, standard work, QA notes)

---

## Recommendation

1. **Wider rollout: do not approve on this pack. Defer the next-quarter funding request by one reporting cycle (4–6 weeks) and re-present.** The blocking issue is the benefit case and several unresolved evidence gaps — **not** camera performance. The operational data supports continuing and, on current evidence, the rollout request is likely to be re-presentable; it is not yet fundable as claimed.
2. **June spend (lines already fitted): Finance's stated test — benefit case ≥ £550k/yr once restated — is not demonstrably met.** Our restatement lands at **£510k on defensibly based lines**, rising to **£558k only if a contested £48k line is accepted** (we do not think it should be, see below). We recommend keeping the fitted lines running under a **time-boxed (2-week) substantiation of the two largest benefit lines (£510k)**, which sit on the one basis this pack shows to be reliable, rather than pulling the spend now.
3. **Correct the record on the headline quality number before the pack circulates.** The W22 slide shows quality **worsening** 4.08 → 4.25 QA rows per 1,000 packs (+4.1%, marked red). That reading is wrong: it is a product-mix artifact. Like-for-like, quality is **flat to improved** (−4.8% at constant mix), with the biggest gains on exactly the lines where the camera's defect classes apply.

---

## 1. What the quality data actually shows

### The headline is a mix artifact (Simpson's paradox)

The W22 roll-up compares a Jan–Feb baseline (242,000 packs, 988 QA rows, 4.08/1,000) with the W16–W21 pilot (262,000 packs, 1,113 rows, 4.25/1,000) across the six main routes (FP1–FP6). Both figures consistently exclude cosmetic/scuff rows (verified: 988 = 769 label/barcode + 51 seal + 168 insert; 1,113 = 817 + 69 + 227), so the numerator basis matches. The denominator mix does not:

| Line (format) | Baseline rate /1,000 | Pilot rate /1,000 | Change |
|---|---|---|---|
| FP1 (STD) | 1.93 | 1.89 | −2.2% |
| FP2 (STD) | 1.90 | 1.89 | −0.5% |
| FP3 (EXP) | 5.20 | 5.30 | +2.0% |
| FP4 (EXP) | 5.05 | 5.14 | +1.8% |
| FP5 (RGD) | 7.88 | 6.63 | **−15.8%** |
| FP6 (RGD) | 7.86 | 6.85 | **−12.9%** |
| **Blended** | **4.08** | **4.25** | **+4.1%** |

No line worsened materially, and the two highest-defect lines improved sharply — yet the blended rate rose, because volume shifted toward the high-rate RGD format (RGD share of packs 19.0% → 26.3%; FP5/FP6 weekly output roughly doubled, 3,000→5,833 and 2,750→5,667 packs/week; STD share fell 48.8% → 41.2%). Re-weighting pilot line rates to the baseline mix gives **3.89/1,000, i.e. −4.8% vs baseline**, reversing the headline.

Two further reasons to treat the like-for-like read as conservative:

- **Detection basis changed between the periods.** The baseline predates any camera (first observe-only build went live 10 Mar; route-hold went live 14–28 Apr per station status), so baseline rows come from the old manual/QA-export detection and pilot rows from the camera-fed MES/QPulse join. A more sensitive detector should inflate pilot counts; rates fell anyway.
- **The class-level "amber" rows overstate.** Seal and insert rows occur only on EXP/RGD formats but the slide rates them against all packs including STD. On the correct denominator they rose ~9% (seal 0.411→0.448, insert 1.355→1.474 per 1,000 EXP/RGD packs) — consistent with the camera finding more, since every one of these cases in QPulse was held and reworked before route close (HELD_REWORKED → ROUTE_CLEAR) and field complaints did not rise.

### The inspection-and-hold mechanism demonstrably works

The full trail for the highest-scoring case (FP6 seal, QP-2556) reconciles end-to-end across five systems: raw camera score 0.93 red → station AUTO_HOLD (EVT-F6-0521-014, 00:18, night shift of 20/05) → pallet-table move (OVR-025) → rework → table close (OVR-026, 02:10) → ROUTE_CLEAR in QPulse, all on LOT-F6A-0520-N2 / PAL-F6-1884. Camera coverage on the six main routes is 100% of sellable packs in MES. The route table remains the release authority throughout — camera clear is never used as ship clear in the records, consistent with SW-44.

### No field (customer) improvement is proven yet

Mature service pull: **12 baseline vs 12 pilot cases** (0.05/1,000 both). The mature pilot cases cover builds W16–W19 only; W20+ builds are still ageing through the complaint window. The "16 cases" received-week figure adds 4 watch rows that reduce to 3 distinct case families, of which only one (CF-WATCH-F6-01, accessory, FP6) is on a main pilot route — the other two are on the trial branches. So: the pilot has not made the field worse, but a field-level benefit cannot yet be claimed. This matters for the finance case (below).

---

## 2. The finance case restated

Original pack £820k/yr; finance's v3 working £806k (after a −£14k case-family cap on the distributor line). Restating line by line against the source data:

| Line | Claimed (v3) | Restated | Why |
|---|---|---|---|
| FIN-001 defect/scrap reduction | £328k | **Keep, subject to substantiation** | Basis (route table + QPulse closed cases + MES) is the one basis this pack shows to be internally consistent. £ value cannot be independently rebuilt from the pack — no cost-per-case rates supplied. |
| FIN-002 avoided internal rework | £182k | **Keep, subject to substantiation** | As FIN-001. |
| FIN-003 distributor rework cases | £48k | **Exclude (contested)** | The mature service data shows **no reduction**: 12 vs 12 cases, flat rate. A claimed reduction contradicted by its own source. |
| FIN-004 manual recheck labour | £54k | **Exclude** | Built on the old recheck export. QA confirm the W17 LS-code change moved support hours out of that field — the before/after is broken, so the "reduction" is at least partly a reporting artifact. Needs restating on the LS basis before any value is claimable. |
| FIN-005 pallet audit staffing removal | £70k | **Exclude** | The pallet table is still in the route on every SW-44 route, and standard work states no final-audit headcount removal is in this request. The benefit assumes a change that has not happened and is not planned here. |
| FIN-006 customer credit reduction | £35k | **Exclude** | The credit rows (CR-CRD-001/002/003) repeat existing service-watch families on the same pallets (3 rows → families already counted), sit on the trial branches, and are credits incurred *during* the pilot — there is no demonstrated reduction. |
| FIN-007 FP8 trial upside | £65k | **Exclude** | F8_TRIAL has no signed release map (SW-DRAFT-8, MAP-HOLD-8T; camera in map-check since 19/05), only 15,810 of 16,800 packs camera-checked (990-pack gap), and it generated a live watch/credit family. Currently negative evidence, not upside. |
| FIN-008 FP5X trial upside | £24k | **Exclude** | Map pending (MAP-PEND-05X), camera in bypass since 19/05, 660-pack coverage gap, live watch/credit family (CR-F5X-114). |
| **Restated total** | | **£510k** (£558k only if FIN-003 is accepted) | vs **£550k sign-off threshold** |

**Position on the June spend:** on the evidence in this pack, the £550k test is not met. £510k of defensible-basis benefit is below the threshold; the £558k pass case depends on a £48k line the service data contradicts. However, the shortfall is small and the two big lines (£510k) sit on the sound basis — so the proportionate step is a time-boxed substantiation of FIN-001/002 (cost-per-case rates against the QPulse HELD_REWORKED population), not an immediate withdrawal of the fitted lines. If FIN-001/002 survive substantiation even approximately intact and any genuine distributor/field benefit emerges as W20+ builds mature, the case clears; if FIN-001/002 shrink materially, it does not, and the June lines should then be re-justified on the corrected quality evidence rather than the bridge.

---

## 3. Records excluded from the like-for-like read, and why

- **FP6 night (F6_NGT):** MC-042's 48,120 packs is almost certainly a **grouped cumulative figure** for the W19–W21 night runs, not a single week: 48,120 = 16,520 (MC-040) + 18,800 (MC-041) + 12,800 residual, and as a single week it would imply 917 packs/hr vs 403–409 in the prior night weeks. Summing MC-040..042 would double-count 35,320 packs. The 810-pack MES-vs-camera gap is explained by the 22/05 00:00–03:45 lens-clean bypass (810 / 3.75h ≈ 216 packs/hr, in line with night rates) — so the count discrepancy is benign, **but ~810 packs shipped route-closed without camera inspection** during the bypass. Excluded from the trend until the night export ties out (as QA requested).
- **FP6-R and FP9 (recovery), FP7 (reference):** recovery sheets sit outside the route table; FP7 is the supplier-compare reference route. The FP7 label-batch rows (QP-2518/2536/2571; CR-SUP-001/002/003 = two case families) trace to supplier batch NB-LBL-25-144 per the supplier notice — supplier noise, not camera or pilot performance, and correctly outside the headline roll-up.
- **FP8-T / FP5X (trial branches):** unsigned maps, partial coverage, prompts-only dispositions (TRIAL_QUEUE). Kept visible per the client's request but not evidence for or against the main-route case.
- **Cosmetic/scuff rows incl. CAM-SCF-11 history:** old-threshold prompt rows retained for trace; excluded consistently from both baseline and pilot numerators (verified), so they do not distort the headline — they only make the cosmetic dashboard view look noisy.
- **Duplicate open cases:** the "10 open QPulse rows" include 3 DUP_LINK rows (QP-2580/2581/2582 duplicate QP-2568/2565/2570 on the same lot/pallet, raised to attach service refs) → **7 distinct open cases**.
- **MC-050:** single calibration-check row, not production.
- The **"continue_wave"** slide footer is a draft-pack artifact, acknowledged as such in the Teams thread; it is not a finding and should be removed before circulation.

---

## 4. Judgment calls and sensitivity

- **Mix adjustment choice:** we re-weighted pilot line rates to the baseline volume mix. The alternative (baseline rates at pilot mix) gives the same direction. Any per-line or constant-mix comparison shows flat-to-improved; only the blended figure shows deterioration.
- **Baseline comparability:** the baseline (6 Jan–28 Feb, ~8 weeks, pre-camera, old QA-export detection) differs from the pilot (6 weeks, camera-fed) in period length, season and detection basis. This is why we anchor on direction and line-level consistency, not the precise −4.8%.
- **FIN-003:** if finance insists on keeping the capped £48k, the case reads £558k — above threshold by 1.5% on a line whose own source shows no change. We would not defend that in front of a board; it is the single choice on which "pass vs fail" turns, which is itself a reason not to fund on this pack.
- **Field read:** "no field improvement" could still reverse in either direction as W20+ builds mature — a genuine remaining unknown, resolvable within the deferral window.

**Bottom line:** the camera system works and the corrected quality evidence is favourable; the money story as packaged is not yet sound. Close the tracker items, restate the bridge, and re-present — likely within one cycle.
