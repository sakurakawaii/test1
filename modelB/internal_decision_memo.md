# Internal decision memo — AI camera inspection pilot, final-pack lines

**Re:** Wider rollout request (next quarter) and June spend table position
**Basis:** W22/W23 pilot pack as received 2025-06-03/04 (19 source files: MES counts, QPulse, station/raw camera exports, customer/service pull, overrides, finance working v3, baseline export, wave tracker, W22 review numbers, QA/supplier notes, ops correspondence)

---

## Recommendation

**Proceed with the wider rollout request — but only for the main-route configuration, and only with the benefit case restated.** Specifically:

1. **GO (conditional)** on wider rollout for the proven pattern: main STD/EXP/RGD routes on signed camera maps (the FP1–FP6 main-route configuration, SW-44A/B/C, MAP-STD-02/EXP-04/RGD-06).
2. **EXCLUDE from the funded scope** the trial and exception branches: FP5X export trial (map unsigned, camera bypassed since 19/05), FP8 trial cartons (draft map, map-hold since 19/05, open seal case with credit exposure), and the FP6 night-exception configuration (count tie-out outstanding). These are not rollout-ready and should not carry benefit value.
3. **Keep the June spend table lines.** The restated, defensible benefit core is **£558k/yr against the £550k sign-off threshold — it passes, but with only £8k (~1.5%) headroom**, and it is contingent on Finance substantiating the two large route-table lines (£510k) line-by-line. That verification should be treated as a condition, not a formality.
4. **Do not circulate the current W22 pack unamended.** Its headline quality figure (+4% deterioration, red) is a mix artifact and is wrong taken at face value; equally, the £820k/£806k benefit figures and the "continue_wave" slide footer are not defensible. Both the pessimistic and the optimistic headline numbers in the pack should be replaced before it goes wider.

---

## 1. The headline quality number is misleading — in the pilot's favour

The W22 slide shows total QA rows per 1,000 packs rising from **4.08 (baseline, 988/242,000)** to **4.25 (pilot, 1,113/262,000)**, marked red (+4.1%). Taken at face value: quality got worse under the camera.

That reading does not survive a per-line look. The pilot window ran a very different product mix from the Jan–Feb baseline:

| Route | Baseline rate /1,000 | Baseline wkly vol | Pilot wkly vol | Pilot rate /1,000 | Change |
|---|---|---|---|---|---|
| FP1 (STD) | 1.93 | 7,500 | ~9,170 | 1.89 | −2.2% |
| FP2 (STD) | 1.90 | 7,250 | ~8,830 | 1.89 | −0.5% |
| FP3 (EXP) | 5.20 | 5,000 | ~7,170 | 5.30 | +2.0% |
| FP4 (EXP) | 5.05 | 4,750 | ~7,000 | 5.14 | +1.8% |
| FP5 (RGD) | 7.88 | 3,000 | ~5,830 | 6.63 | **−15.8%** |
| FP6 (RGD) | 7.86 | 2,750 | ~5,670 | 6.85 | **−12.9%** |

RGD and EXP formats intrinsically carry ~3–4× the QA-row rate of STD (they have seal and insert/accessory checks; STD shows none in either period), and the RGD lines roughly **doubled** their weekly volume in the pilot window. Holding each line at its baseline rate, the pilot mix would have produced ~1,186 QA rows (4.53/1,000). Actual was 1,113 (4.25/1,000) — **a mix-adjusted improvement of ~6%**, driven by the RGD routes, with STD flat and EXP marginally up. The blended +4% "red" is Simpson's paradox, not deterioration.

**Caveats on this comparison (stated because the conclusion depends on them):** (a) the detection basis changed — baseline rows come from the manual QA export (Jan–Feb), pilot rows from the camera-fed MES/QPulse join, so part of any movement could be detection rather than true quality; (b) the route-hold feed only went fully live 28/04 (start of W18), part-way through the W16–W21 pilot window used in the rollup. We therefore treat the −6% as *indicative*, not proven. What the data does firmly support is the narrower statement: **there is no evidence of quality deterioration under the camera, and the slide's red flag is an artifact.** Both numerators exclude cosmetic/scuff rows on the same basis (verified: baseline 988 = label+seal+insert; pilot 1,113 likewise), so the class composition is like-for-like.

## 2. The seal/insert "amber" rises are overstated and represent detection, not escapes

The slide shows seal rows 0.21→0.26/1,000 (+24%) and insert rows 0.69→0.87 (+26%). Both are divided by **total** packs including STD, which has no seal/insert checks in either period. Against the correct denominator (EXP+RGD packs only): seal 0.411→0.448 (**+8.9%**), insert 1.355→1.474 (**+8.8%**).

More importantly, these are counts at the detection layer. All 11 closed seal/insert cases on main routes in the pilot window were dispositioned **HELD_REWORKED → ROUTE_CLEAR** — caught and fixed before release. The highest-scoring case (QP-2556, FP6 seal band) shows the intended workflow end-to-end: camera auto-hold 00:18, pallet table 00:42 (OVR-025), reworked and route-closed 02:10 (OVR-026), QA case closed that morning. (Note: its calendar date is 21/05 but shift date 20/05 night — the known midnight-read point; it is one case, not two.) A camera that fires somewhat more often on export/rigid formats and contains everything it fires on is consistent with the system doing its job.

## 3. Field outcomes are neutral so far — not yet evidence of benefit

Mature customer cases: **12 baseline vs 12 pilot (~0.05/1,000), flat.** Two qualifications:

- **The pilot field read is immature.** 6 of the 12 pilot-period cases are from builds W16–W17, *before* the route-hold feed went live (28/04); builds from W20–W21 have not yet aged through the normal field window (4 service-watch rows still ageing, one a repeat of an existing family). The received-week view of 16 should not be compared to the mature 12.
- **Traceability of the "linked QP" refs is weak.** On 10 of the 12 mature pilot cases, the linked QPulse ref points at a *different* lot and pallet (same route and defect class only) — these are class-level associations, not evidence the camera saw and missed those specific packs. Two cases genuinely trace to pallets the camera held and the table reworked (CR-PIL-010 → QP-2531, PAL-F5-5169 seal; CR-PIL-012 → QP-2537, PAL-F6-1849, though the complaint class differs). Those two warrant a rework-effectiveness check (tracker item A3).

So the honest field statement is: **no deterioration, no demonstrated improvement yet.** The rollout case currently rests on internal containment and the mix-adjusted internal trend, not on field escape reduction. (Minor: the 244,000 pack denominator used in the service rollup rows could not be reconciled to any MES sum — immaterial at 0.05/1,000 either way, but flagged.)

## 4. The benefit case: £820k/£806k is not defensible; the defensible core is £558k

Finance's own threshold for keeping the June table lines is **£550k/yr restated**. Line-by-line:

| Line | Claimed | Status |
|---|---|---|
| FIN-001 defect/scrap reduction (main routes) | £328k | **Carry, subject to verification** — route-table bridge; not independently rebuilt from this extract |
| FIN-002 avoided internal rework (main routes) | £182k | **Carry, subject to verification** — as above |
| FIN-003 distributor rework cases | £62k → **£48k** | Carry at v3 value (case-family cap correctly applied) |
| FIN-004 manual recheck labour | £54k | **Remove until restated** — the W17 QA export change moved support hours under the LS code; the old recheck extract is not a clean before/after (QA notes §1/§6 say exactly this) |
| FIN-005 pallet-audit staffing removal | £70k | **Remove** — contradicted by standard work: the pallet table is still in every main route, and the extract states no final-audit headcount change is in this request. This saving has not happened |
| FIN-006 customer credit reduction | £35k | **Remove** — the credit rows (CR-CRD-001..003) duplicate existing service-watch case families and sit entirely on trial lines |
| FIN-007/008 FP8 + FP5X trial upsides | £89k | **Remove from rollout case** — unsigned maps, branches not released to the normal route table |

**Restated core: £328k + £182k + £48k = £558k ≥ £550k.** The June spend table stands — but the margin is £8k, and £510k of the £558k is carried from the pack's route-table bridge rather than independently verified here. If FIN-001/002 lose more than ~1.5% under restatement, the June table fails the threshold. That verification is the single most important open action.

## 5. What is not rollout-ready (and why it must be carved out of scope)

- **FP5X (export trial):** camera map unsigned (MAP-PEND-05X), station in bypass since 19/05, coverage 10,940/11,600 packs (94.3%). The 660 "pack gap" is unchecked packs, not lost production.
- **FP8 (trial cartons):** draft map only (SW-DRAFT-8), station on map-hold since 19/05, coverage 15,810/16,800 (94.1%), open trial seal case QP-2568 with service-watch and credit family CR-F8-238 still live.
- **FP6 night exception:** lens-clean on 22/05 left an 810-pack camera count gap (MES 48,120 vs camera 47,310 — a coverage gap during the 00:00–03:45 bypass, not missing product), and the 48,120 "grouped night run" itself has not been tied out against the ~16.5–18.8k of prior night weeks. QA has correctly held it out of the trend; it was not in the 262k rollup.
- **FP7 label noise is a supplier issue, not camera performance:** QP-2518/2536/2571 and CR-SUP-001..003 all belong to the Northbank batch NB-LBL-25-144 family (two case families, not six incidents). FP7 is a reference line and is correctly outside the rollup; keep it out of camera KPIs.
- **Record hygiene:** QP-2580/2581/2582 are DUP_LINK rows duplicating existing case families — the true open-case count is 7, not the 10/43 (23.3%) shown on W22-027. The 4 CAM-SCF-11 scuff rows are history/trace only (2 of them calibration rows) and sit in neither headline numerator — verified; they affect the dashboard's appearance, not the numbers.

## 6. Judgment calls made, and what an alternative would do

- **Pilot window:** we used the pack's own W16–W21 rollup. Restricting to fully-live weeks (W18–W21) would likely flatter the camera slightly; we did not, to stay comparable with the pack.
- **Mix adjustment:** we held per-line baseline rates constant and reweighted to pilot volumes. Any reasonable standardisation (either direction) gives the same sign: the blended +4% disappears once mix is controlled.
- **Finance exclusions:** each removed line is removed for a stated evidential reason, not prudence padding. The only line where reasonable people could differ is FIN-004 (£54k) — *restatable* rather than wrong; if even half survives restatement the headroom roughly quadruples. Conversely, the case should not be presented as depending on it.
- **Field read:** we treated "flat 12 vs 12" as neutral/immature rather than as either success or failure; claiming either would outrun the data.

## 7. Bottom line

The operational data is **neutral-to-positive once read at the right level** (per-line, correct denominators, containment dispositions), the apparent deterioration in the pack is an artifact, and the restated benefit case clears the sign-off bar with minimal headroom. That supports **keeping the rollout request moving for main-route configurations and keeping the June spend lines**, with the trial/night branches explicitly descoped and the conditions in the action tracker (notably finance substantiation of FIN-001/002 and the FP6 night tie-out) closed before the pack is circulated more widely.
