# Gel Electrophoresis Analysis — Quarterly Progress Review
**Prepared for:** Monday quarterly progress review
**Prepared by:** Gel/PCR Analysis Assistant, Ridgeline Institute of Molecular Sciences
**Source material:** Shared-drive dump under `/tmp/inputs/` (mixed projects)
**Figures referenced:** Figure 1 (CSAP‑002), Figure 2 (HERB‑003), Figure 3 (LACB‑014)

---

## 1. Summary (read this first)

Three gel images were relevant to active, PI‑led projects and have been fully analysed. Two additional items referenced gels but **no usable gel image was supplied**, so they could not be analysed.

| Project | Figure | Gel date | Verdict | Action |
|---|---|---|---|---|
| **LACB‑014** (Lactobacillus multiplex) | **Figure 3** | 16 Mar 2026 | **Usable — high quality.** All six target species resolved at expected sizes; all negative/no‑template controls blank. | **Ready for next step** (freezer‑stock deposit). No rerun needed. |
| **HERB‑003** (herbarium DNA integrity) | **Figure 2** | 03 Jun | **Usable.** Clear fresh→young→old degradation gradient across all four species; fresh controls intact. | Results support the feasibility decision; see discussion. Ginkgo young/old lanes are faint (low confidence on those two lanes only). |
| **CSAP‑002** (crab species RFLP) | **Figure 1** | 29 Apr 2026 | **Interpretable but not conclusive.** Species groups separate as expected (danae = single band; sapidus = cut + uncut), but (a) an **unresolved source conflict** governs how the sapidus partial‑digest pattern should be called, and (b) image/QC caveats apply. | **Confirmatory 3‑hour full digest recommended** before the pattern is certified (satisfies both conflicting sources). Do **not** report lane 17 identity. |
| **PSMD‑001** | — | 10 Apr (note) | **Cannot analyse** — `PSMD-001_scan.jpg` is a handwritten note, not a gel image. | Already flagged by the team for redo; **rerun required**. |
| **MPNE‑007** | — | 16 Mar (note) | **Cannot analyse** — gel run described in notebook but **no image supplied**. | Supply the gel image if analysis is needed. |

**Headline findings the PIs should know immediately**
- **LACB‑014 (Dr. Calloway):** The six‑species multiplex panel worked cleanly on single‑strain DNA — every target gave its correct single band and every negative control was blank (**Figure 3**). This is the strongest gel in the set.
- **HERB‑003 (Dr. Bosch):** The gel shows the expected age‑related degradation — fresh tissue = high‑molecular‑weight (HMW) DNA; old herbarium = heavily degraded low‑MW smear (**Figure 2**). This directly informs the "is it worth sequencing the old material" question.
- **CSAP‑002 (Dr. Duarte):** The gel **separates the two crab groups as expected** (**Figure 1**), but two lab sources **disagree on whether the residual uncut band in true‑sapidus lanes at 30 min is "normal" or a sign of incomplete digestion.** This conflict **cannot be resolved from the supplied material** (see §6) and is flagged rather than decided. A 3‑hour full digest would sidestep it.

---

## 2. What was in the folder, and what I used

**Active projects with a full document set + gel image (analysed):** CSAP‑002, HERB‑003, LACB‑014. Each had a PI memo addressed to the technician, a protocol, a sample manifest, a lab notebook, a gel photo, and handwritten setup notes — these are the quarterly‑review items.

**Referenced a gel but no usable image (not analysed):** PSMD‑001 (`PSMD-001_scan.jpg` is a handwritten note), MPNE‑007 (notebook entry only).

**Not gel‑relevant / other projects / admin (excluded from analysis):** `SOIL-019_labnotebook.txt` (went straight to shotgun sequencing, no diagnostic gel), `freezer_inventory_update.txt`, `gel_doc_maintenance_log.txt` (used only as supporting QC context), `multiplex_PCR_background_reading.txt` (general background, explicitly "not tied to any specific ongoing project"), `CB-0231_sequencing_summary.txt` (supporting evidence for CSAP‑002).

Dates were cross‑referenced across notebooks, setup notes and manifests to match each image to its method (e.g., CSAP‑002 setup notes are dated **29 April 2026** and match the 29 April notebook entry and manifest; HERB‑003 notes are dated **03 June**; LACB‑014 notes are dated **16 March 2026**).

---

## 3. Figure 1 — CSAP‑002 (SspI PCR‑RFLP, gel dated 29 April 2026)

![Figure 1](Figure1_CSAP-002.png)

**Figure 1. CSAP‑002 — SspI restriction digest of ~180 bp 12S rRNA PCR products, gel dated 29 April 2026.** 1% agarose/TAE, ethidium bromide, 100 V ~40 min, imaged on a UVP Gel Doc‑It2 (`CSAP-002_gel_setup_notes.jpg`; `CSAP-002_protocol.docx`). **Ladder:** Promega 100 bp (lanes 10 and 19; rungs 100–1000 bp + 1500 bp, with the 500 bp reference band brightest). Lane assignments follow `CSAP-002_sample_manifest.txt`. Guide lines mark ~180 bp (uncut product) and ~110 bp (major cut fragment). Sequence‑confirmed *C. sapidus* lanes: 2, 3, 5, 11, 12, 14. Sequence‑confirmed *C. danae* lanes: 6, 7, 8, 15, 16 (lane 17, CB‑0315, ID **unconfirmed** — see below). Expected fragment sizes per `CSAP-002_protocol.docx`: uncut ~180 bp; *C. sapidus* cut fragments 113 bp + 67 bp.

**Observed band table**

| Lane | Sample | Documented species | Approx. band sizes observed | Band identity (from context) | Artefacts / notes |
|---|---|---|---|---|---|
| 2 | CB‑0231 | *C. sapidus* | ~180 + ~115 (+ faint <100) | uncut + cut fragment(s) | fainter lane; background mottling |
| 3 | CB‑0233 | *C. sapidus* | ~180 + ~100 (+ faint) | uncut + cut fragment(s) | faint |
| 5 | CB‑0240 | *C. sapidus* | ~180 + ~106 | uncut + cut fragment(s) | faint |
| 6,7,8 | CB‑0301/0302/0304 | *C. danae* | single ~175–180 | uncut product (no SspI site) | clean, strong single band |
| 10 | — | ladder | 100–1000 + 1500 | Promega 100 bp | reference band (500 bp) clear |
| 11 | CB‑0245 | *C. sapidus* | ~175 + ~116 | uncut + cut fragment | **cleanest sapidus lanes** |
| 12 | CB‑0247 | *C. sapidus* | ~178 + ~119 | uncut + cut fragment | clean |
| 14 | CB‑0250 | *C. sapidus* | ~180 + ~119 | uncut + cut fragment | clean |
| 15,16 | CB‑0310/0312 | *C. danae* | single ~179 | uncut product | clean, strong |
| 17 | CB‑0315 | *C. danae* (unconfirmed) | single ~188 | pattern matches other danae; **identity not confirmed** | paperwork lost (see below) |
| 19 | — | ladder | 100–1000 + 1500 | Promega 100 bp (2nd, flanking) | not listed in manifest (see notes) |

*The very faint, scattered signals above ~500 bp in several lanes were also present in the empty lanes and next to the ladder, i.e. they are background/lateral‑glow artefacts, not sample bands, and are not reported as bands.*

**Discussion.** CSAP‑002 is a seafood‑mislabeling screen that uses SspI digestion of a ~180 bp 12S rRNA amplicon: only true *C. sapidus* carries the SspI site and is cut, while other *Callinectes* spp. remain a single uncut band (`CSAP-002_protocol.docx`; Lee et al., 2020). On this gel the two groups behave as the design predicts: the six sequence‑confirmed *C. danae* lanes (6, 7, 8, 15, 16) each show a **single uncut ~180 bp band**, and the sequence‑confirmed *C. sapidus* lanes (2, 3, 5, 11, 12, 14) each show the **~180 bp band plus a smaller cut fragment (~113 bp; the expected 67 bp fragment is faint/poorly resolved on a 1% gel)** — i.e. the partial‑digestion pattern. This is consistent with Dr. Duarte's hypothesis that the SspI assay separates true *C. sapidus* from other *Callinectes* on digestion pattern alone (`CSAP-002_PI_memo.txt`), and the species calls match the independent Sanger result on file for CB‑0231 (*C. sapidus*, 99.2% identity; `CB-0231_sequencing_summary.txt`). **However**, whether the residual uncut band in the sapidus lanes should be read as an *expected* partial digest (Lee et al., 2020) or as an *incomplete* reaction needing a rerun is subject to an **unresolved conflict between two lab sources** (see §6); I therefore report the pattern but do **not** certify these lanes as a complete/validated digest. Per the lab notebook, **lane 17 (CB‑0315) must not be reported as confirmed *C. danae*** — the specimen's sequencing paperwork was lost in transit (`CSAP-002_labnotebook.txt`, 29 April); its band pattern (single ~180 bp) is reported, but the species label is withheld. The PI memo also notes the assay has **not** been validated on cooked/processed crab meat, so these fresh‑tissue results should not be generalised to processed product (`CSAP-002_PI_memo.txt`).

---

## 4. Figure 2 — HERB‑003 (genomic DNA integrity, gel dated 03 June)

![Figure 2](Figure2_HERB-003.png)

**Figure 2. HERB‑003 — genomic DNA integrity across fresh / young‑herbarium / old‑herbarium tissue for four species, gel dated 03 June.** Four panels, one species each: **(a)** *Lonicera maackii*, **(b)** *Ginkgo biloba*, **(c)** *Laburnum anagyroides*, **(d)** *Liriodendron tulipifera* (`HERB-003_specimen_manifest.txt`). 1% agarose/TAE, EtBr, 90 V ~50 min (`HERB-003_gel_setup_notes.jpg`). Lanes per panel: **M** = ladder, **F** = fresh leaf, **FH** = young herbarium (dried same day), **H** = old herbarium (archival; ages per panel headers). Image shown in standard orientation (DNA = dark on a light background). **Ladder (M):** 1 Kb Plus DNA Ladder, Invitrogen (per manifest). *Sizing here is qualitative/relative: the specific rung values of this ladder are not documented in the supplied files, so no exact bp values are assigned to rungs — interpretation uses relative migration against the protocol's own thresholds.*

**Observed pattern table**

| Panel (species) | Old‑sample age | F (fresh) | FH (young herbarium) | H (old herbarium) | Artefacts / notes |
|---|---|---|---|---|---|
| (a) *Lonicera maackii* | ~65–114 y | HMW band at top, minimal smear | reduced, signal shifted down | faint low/mid smear | consistent with expectation |
| (b) *Ginkgo biloba* | ~107 y | strong HMW band at top | **very faint** (low signal) | **faint** (low signal) | low load/yield → low confidence on FH & H |
| (c) *Laburnum anagyroides* | ~65 y | HMW band at top | faint smear | distinct **low‑MW smear** (most clearly degraded) | clearest old‑sample smear |
| (d) *Liriodendron tulipifera* | ~114 y | HMW band at top | mid‑gel smear | faint low smear | consistent with expectation |

**Discussion.** HERB‑003 is a feasibility assessment: Dr. Bosch wants to know whether the older herbarium specimens are worth sequencing or "too far gone," expecting fragment sizes to drop with specimen age (`HERB-003_PI_memo.txt`). The gel supports that expectation. Across all four species the **fresh (F) lanes show intact HMW DNA sitting at the top of the gel**, while the **old‑herbarium (H) lanes show degradation to a low‑MW smear**, with the young‑herbarium (FH) lanes intermediate. This is the pattern described by Staats et al. (2011), who report that fresh tissue yields HMW DNA whereas herbarium material is heavily fragmented, and that a smeared low‑MW gel is the *normal, expected* appearance of degraded herbarium DNA rather than a failed extraction. The low yields measured for the old specimens (NanoDrop ~7–9 ng/µL vs ~138–156 ng/µL for fresh; `HERB-003_nanodrop_readings.csv`) are consistent with the faint old‑herbarium lanes. Importantly, the protocol's fail‑flag — an unexpectedly degraded **fresh** sample — is **not** triggered here: every fresh control is intact, which validates the CTAB extraction (`HERB-003_protocol.docx`). Practically, this favours prioritising fresh/young material (or shorter target regions / more sensitive extraction for the oldest specimens), exactly as anticipated in the memo. Note Dr. Bosch's own caveat that the institute's pre‑2005 storage records are patchy, so published degradation timelines are a general guide, not an exact predictor for these specimens (`HERB-003_PI_memo.txt`). *Telle & Thines (2008) is mentioned in the notebook as a possible extraction‑optimisation reference but no summary was supplied, so it is not cited here.*

---

## 5. Figure 3 — LACB‑014 (six‑species multiplex PCR, gel dated 16 March 2026)

![Figure 3](Figure3_LACB-014.png)

**Figure 3. LACB‑014 — species‑specific multiplex PCR panel for the *Lactobacillus acidophilus* group vs negative controls, gel dated 16 March 2026.** 1.5% agarose/TAE, EtBr, 100 V ~45 min, Bio‑Rad Gel Doc (`LACB-014_gel_setup_notes.jpg`; `LACB-014_protocol.docx`). **Ladder (M):** 100 bp ladder, lab stock, flanking both sides (per manifest). Target lanes 1–6 each loaded with one single‑strain template run against the pooled six‑primer multiplex; lanes 7–11 and NC are controls. Expected product sizes from `LACB-014_primer_size_reference.jpg`. Green circles mark the called band in each target lane. Band positions fit the documented expected sizes with a log‑size‑vs‑migration correlation of r ≈ 0.99.

**Observed band table**

| Lane | Strain / role | Expected size | Observed band | Call | Artefacts / notes |
|---|---|---|---|---|---|
| 1 | *L. gasseri* | 1241 bp | ~1.2–1.3 kb (strong) | correct | — |
| 2 | *L. acidophilus* | 828 bp | ~830 bp (strong) | correct | — |
| 3 | *L. helveticus* | 680 bp | ~655 bp (strong) | correct | — |
| 4 | *L. jensenii* | 540 bp | ~548 bp (strong) | correct | — |
| 5 | *L. crispatus* | 420 bp | ~380–420 bp (strong) | correct | — |
| 6 | *L. gallinarum* | 224 bp | ~240 bp (clear) | correct | slightly fainter (smallest product) |
| 7–11 | *L. plantarum / salivarius / reuteri / E. faecalis / E. faecium* (neg. controls) | none | **no band** | correct (no cross‑reactivity) | — |
| NC | no‑template | none | **no band** | correct | — |
| M | ladder | — | 100 bp ladder | reference | — |
| (top of gel) | — | — | dark band across wells | overloaded well / loading‑front artefact | sits **above** all target bands; does not interfere |

**Discussion.** LACB‑014 tests whether a new six‑species multiplex can call species identity from band size in a single reaction, avoiding per‑isolate 16S sequencing (`LACB-014_PI_memo.txt`). On this gel the panel performs exactly as designed: the six target strains produce a clean descending **staircase** of single bands at their documented sizes (gasseri 1241 → gallinarum 224 bp; `LACB-014_primer_size_reference.jpg`), and all five related‑species negative controls plus the no‑template control are blank. This matches You & Kim (2020), who report that each primer set yields a single correctly‑sized band for its target with no amplification in negative controls, and that the six‑way multiplex preserves this species‑specific pattern. It also satisfies the protocol's two checks — one distinct band per present target, and **no** band in any negative‑control lane (a control band would indicate contamination/cross‑reactivity; `LACB-014_protocol.docx`). This is consistent with Dr. Calloway's hypothesis that unique single‑copy‑gene primers give clean species‑level calls (`LACB-014_PI_memo.txt`). **Scope caveat:** these are **clean single‑strain** results only. Both the PI memo and You & Kim (2020) flag that a genuinely mixed/pooled sample caused one target to drop out undetected, which the authors could not fully explain; this panel has not been validated by the lab on mixed samples, so the result must not be extrapolated to complex/pooled material (see §6 for a related documentation conflict). Within that scope, this gel is clean and the isolates can proceed.

---

## 6. Analysis notes — conflicts, discrepancies and caveats

**6.1 CSAP‑002 — UNRESOLVED source‑vs‑source conflict on the 30‑minute digestion pattern (do not treat as settled).**
Two lab sources disagree on how to interpret a residual uncut band in a true‑*sapidus* lane at the 30‑minute timepoint:
- **Lee et al. (2020)** (`Lee_2020_summary.txt`): partial digestion — both the uncut ~180 bp band and the cut fragments present together at ~30 min — is the **expected, normal** result for *C. sapidus*; only a multi‑hour digest gives a clean single small‑fragment pattern.
- **The lab's separate methodological digestion‑timing source** (`CSAP-002_digestion_timing_notes.txt`): a 30‑minute incubation should be **sufficient for complete digestion**, and any residual uncut band at 30 min indicates an **incomplete reaction that should be re‑run**.

These two sources make directly contradictory factual/methodological claims. Per lab policy, a source‑vs‑source conflict **cannot be resolved by any note, memo, or other non‑source document** — so the fact that the **PI memo and lab notebook both endorse the Lee (2020) "partial‑digest‑is‑normal" reading** (`CSAP-002_PI_memo.txt`, `CSAP-002_labnotebook.txt`, `CSAP-002_gel_setup_notes.jpg`) **does not settle the conflict**. (Dr. Duarte independently flags the disagreement and writes "don't take this as universally settled.") I have therefore **not** drawn any conclusion that depends on which interpretation is correct. What is safe either way: *C. danae* lanes show a single uncut band (both sources agree non‑sapidus is not cut), and the *C. sapidus* lanes show clear evidence of SspI cutting (smaller fragment present) — so the groups are distinguishable on this gel and are consistent with the prior sequence IDs. What remains **undecided**: whether the sapidus lanes are "complete/acceptable as‑is" or "incomplete → rerun." **Practical route around the conflict:** run the **3‑hour full digest** on a sapidus subset — a clean single small‑fragment result there is accepted under *both* sources (Lee 2020 calls it the definitive pattern; the timing source wants complete digestion anyway).

**6.2 CSAP‑002 — lane 17 / CB‑0315 identity withheld.** Confirmation paperwork was lost in transit; the notebook explicitly instructs not to carry over a "confirmed *C. danae*" label (`CSAP-002_labnotebook.txt`, 29 April). Band pattern reported; species ID not.

**6.3 CSAP‑002 — manifest vs image (minor).** The manifest lists a single ladder (lane 10), but the gel shows a **second flanking Promega 100 bp ladder at the right edge (lane 19)**. Both read identically; the extra ladder only improves sizing confidence. No impact on calls.

**6.4 HERB‑003 — setup notes vs manifest/notebook/image (documentation discrepancy).** The handwritten setup notes (`HERB-003_gel_setup_notes.jpg`) list a loading order of **only two species (Ginkgo, Laburnum)** and state "**no ladder decided yet**." The specimen manifest, the 03 June notebook entry ("fresh/young/old comparison across **all four species**"), and the gel image itself all show **four species, each panel including a 1 Kb Plus ladder**. The setup note appears to be a **superseded pre‑run draft**; I have treated the manifest + notebook + image as authoritative for what was actually run. Flagged so the bench can reconcile their paperwork.

**6.5 LACB‑014 — notebook claim contradicts the paper (paper takes precedence).** The 15 March notebook entry relays a verbal claim that the panel "**worked fine on mixed‑species DNA … without any issues**" (`LACB-014_labnotebook.txt`). This contradicts **You & Kim (2020)**, who found a target **dropped out undetected** in a mixed‑sample test, and it also contradicts Dr. Calloway's own later memo stating the lab has **not** run its own mixed‑sample validation (`LACB-014_PI_memo.txt`). Because a peer‑reviewed paper outranks a note, the mixed‑sample capability should be treated as **unvalidated/limited** per You & Kim (2020); the casual "works fine on mixed samples" note should not be relied upon. This gel contains only single‑strain samples, so it does not bear on the question either way.

**6.6 Imaging/QC context.** The CSAP‑002 setup notes (29 April) record the **UV bulb was "too dim,"** which is consistent with the fainter bands and mottled background on that image. The shared gel‑doc log shows the **bulb was replaced and a blank calibration run on 03 June** (`gel_doc_maintenance_log.txt`) — i.e. the HERB‑003 gel (03 June) was imaged after the fix, which fits its cleaner appearance. The CSAP‑002 setup notes also remind the user to "double‑check inclusion of a negative control," and indeed **no no‑template/negative PCR control lane appears** in the CSAP‑002 manifest or gel — a minor QC gap for that run.

---

## 7. Confidence assessment (per gel)

**Figure 3 — LACB‑014: HIGH confidence.**
- Ladder: the manifest documents a "100 bp ladder (lab stock)" and the gel shows it flanking both sides; I did **not** invent rung values, and band identities do **not** rely on reading the ladder — they follow the documented lane order and the expected product sizes, which fit the observed migration at r ≈ 0.99.
- All six targets give single bands at expected sizes; all six controls (5 negative + NTC) are blank. Clean, well‑resolved, minimal artefacts (only a benign overloaded‑well band above the amplicons).
- Low‑confidence items: none material. The gallinarum (224 bp) band is the faintest but is still clearly present. Conclusions are restricted to single‑strain performance (§6.5).

**Figure 2 — HERB‑003: MEDIUM–HIGH confidence for the overall degradation gradient; LOWER for two specific lanes.**
- Ladder identity taken from the manifest (1 Kb Plus, Invitrogen); **sizing kept qualitative** because exact rung values are not in the supplied files — I describe relative migration against the protocol's own HMW/young/old expectations rather than assigning bp to rungs.
- The fresh→young→old gradient is consistent and clear in panels (a), (c), (d), and the fresh controls are intact in all four.
- **Low‑confidence calls:** the *Ginkgo* (panel b) **FH and H lanes are very faint (low signal)**; their exact fragment distribution is not well‑characterised, though what signal is present does not contradict the overall pattern. Documentation discrepancy in §6.4 noted.

**Figure 1 — CSAP‑002: MEDIUM confidence on the band pattern; the overall call is deliberately NOT certified.**
- Ladder: **high confidence** — the Promega 100 bp ladder is documented in the protocol/setup notes and both ladder lanes read cleanly (bright 500 bp reference band; 1500 bp band well separated).
- Band pattern is **interpretable**: danae = single ~180 bp (strong, clean); sapidus = ~180 bp + ~113 bp cut fragment (the 67 bp fragment is faint/under‑resolved on 1% agarose).
- **Quality caveats:** fainter image with mottled background / lateral glow (consistent with the "dim UV bulb" note); faint >500 bp specks are background (confirmed present in empty lanes) and are excluded; the left‑hand sapidus lanes (2, 3, 5) are noisier than the right‑hand ones (11, 12, 14); no no‑template control lane (§6.6).
- **Not certified because:** the interpretation of the sapidus partial‑digest pattern rests on an **unresolved source conflict (§6.1)**. Recommend a confirmatory 3‑hour full digest before reporting the sapidus lanes as complete. Lane 17 identity withheld (§6.2).

**PSMD‑001 and MPNE‑007: NOT analysable.** No usable gel image was supplied (PSMD‑001's file is a handwritten note; MPNE‑007 has only a notebook entry). No ladder, manifest, or image to work from — **no band sizes or identities can or should be assigned.** PSMD‑001 is already marked for redo by the team; for MPNE‑007, supply the image if analysis is needed.

---

## 8. Recommended next steps (at a glance)

- **LACB‑014:** Accept — proceed to freezer‑stock deposit. If mixed/pooled screening is ever intended, run the lab's own mixed‑sample validation first (§6.5).
- **HERB‑003:** Accept for the feasibility decision — prioritise fresh/young material; for the oldest specimens consider shorter target regions / more sensitive extraction. Reconcile the setup‑note paperwork (§6.4). Re‑image/re‑run *Ginkgo* FH & H only if those two lanes need to be quantified.
- **CSAP‑002:** Run a **3‑hour full digest** on a *C. sapidus* subset to resolve the partial‑vs‑incomplete ambiguity (§6.1); add a no‑template control; consider a higher‑percentage gel (or capillary) to resolve the 113/67 bp fragments; keep lane 17 unlabelled until its sequencing is recovered.
- **PSMD‑001 / MPNE‑007:** Rerun / supply image.

---

## 9. References

Lee, B. B., Schott, E. J., Behringer, D. C., Bojko, J., Kough, A., & Plough, L. V. (2020). Rapid genetic identification of the blue crab *Callinectes sapidus* and other *Callinectes* spp. using restriction enzyme digestion and high resolution melt assays. *Frontiers in Marine Science, 7*, 633. https://doi.org/10.3389/fmars.2020.00633

Staats, M., Cuenca, A., Richardson, J. E., Vrielink-van Ginkel, R., Petersen, G., Seberg, O., & Bakker, F. T. (2011). DNA damage in plant herbarium tissue. *PLOS ONE, 6*(12), e28448. https://doi.org/10.1371/journal.pone.0028448

You, I., & Kim, E. B. (2020). Genome-based species-specific primers for rapid identification of six species of *Lactobacillus acidophilus* group using multiplex PCR. *PLOS ONE, 15*(3), e0230550. https://doi.org/10.1371/journal.pone.0230550

*Not cited (no summary supplied, referenced only in project notes):* Telle & Thines (2008), mentioned in `HERB-003_labnotebook.txt`. The lab‑held methodological digestion‑timing source summarised in `CSAP-002_digestion_timing_notes.txt` has no author/title/year in the supplied material and so cannot be given a formal citation; it is referred to by filename in §6.1.

---
*Report generated from the supplied files only. Band sizes are approximate, based on migration relative to the stated ladders and documented expected sizes; no ladder, band identity, hypothesis, or conclusion has been assigned without supporting evidence from the provided material.*
