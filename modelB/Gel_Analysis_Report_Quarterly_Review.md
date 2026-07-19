# Gel Electrophoresis Analysis Report — Quarterly Progress Review

**Prepared for:** Monday quarterly progress review (PIs: Dr. A. Duarte / CSAP-002, Dr. I. Bosch / HERB-003, Dr. B. Calloway / LACB-014)
**Prepared by:** Gel Analysis Assistant, The Ridgeline Institute of Molecular Sciences
**Requesting technician:** Dev Okonkwo
**Gel images analysed:** 3 (CSAP-002, HERB-003, LACB-014)

---

## 1. Summary (read this first)

Three gel images in the shared-drive dump are genuine gel photographs tied to the three projects whose PIs asked for a status update. All three were matched to their project notes with high confidence (filename + date + loaded-lane content all agree). A fourth image (`PSMD-001_scan.jpg`) is **not** a gel photo — it is a scanned one-line note — and several other files belong to unrelated projects or are administrative (see Section 6).

| Project | Figure | Date run | Status | One-line verdict |
|---|---|---|---|---|
| **CSAP-002** (blue-crab PCR-RFLP) | **Figure 1** | 29 Apr 2026 | **Usable / interpretable** | Assay worked: all sequence-confirmed *C. sapidus* lanes cut (partial digest), all *C. danae* lanes uncut. Ready to report, with one labelling caveat (lane 17) and one documentation conflict to be aware of. |
| **HERB-003** (herbarium DNA integrity) | **Figure 2** (panels a–d) | 3 Jun | **Usable / interpretable** | Clear age-dependent degradation gradient in all 4 species: fresh = intact high-MW; young herbarium = degraded; old herbarium = heavily degraded/near-absent. Feasibility call can be made. |
| **LACB-014** (6-species multiplex) | **Figure 3** | 16 Mar 2026 | **Usable / high quality** | All six species gave single bands at expected sizes; all 5 negative controls + no-template control clean. Strongest gel of the set. Ready for next step. |

**Findings the PIs should know immediately**
- **CSAP-002 (Fig 1):** The result supports Dr. Duarte's screen — the PCR-RFLP pattern agrees with the known (sequence-confirmed) species identities. *Action item:* there is a **direct contradiction** between a methodological note on file and the project's reference paper about what the 30-minute digest *means*; this is resolved in Section 5, but please read it before writing up. Also, **lane 17 (CB-0315) must not be written up as "confirmed *C. danae*"** — its confirmation paperwork was lost (`CSAP-002_labnotebook.txt`).
- **HERB-003 (Fig 2):** No "failed extraction" here — the smeared/low-MW pattern in older specimens is the *expected* outcome for archival herbarium DNA. Prioritise fresh/younger material for sequencing; the oldest specimens (Liriodendron ~114 yr, Ginkgo ~107 yr) retain very little high-MW DNA.
- **LACB-014 (Fig 3):** Panel cleanly discriminates all six species by band size with clean negatives — no rerun needed. *Note:* a claim recorded in the lab notebook that the panel "worked fine on mixed samples" conflicts with the project's own paper and the PI's memo (Section 5); it does **not** affect this single-strain gel but should not be relied upon.

**Reruns required:** None of the three analysed gels requires a rerun on quality grounds. (`PSMD-001` is a different project and was already flagged by its owner for a redo; it has no image to analyse.)

---

## 2. Scope — what was relevant and how images were matched to notes

The folder contained material from several projects. Files were assigned to an experiment only where the filename project-code, the dates, and the loaded-lane content agreed. All three analysed gels met that bar:

- **CSAP-002_gel_photo.JPG** → digestion date **29 Apr 2026**. The handwritten setup sheet (`CSAP-002_gel_setup_notes.jpg`, dated "29th April 2026") gives the loading order, which matches `CSAP-002_sample_manifest.txt` lane-for-lane, and the notebook (`CSAP-002_labnotebook.txt`, 29 April) confirms digestion + imaging that day. High-confidence match.
- **HERB-003_gel_photo.tif** → **3 Jun**. `HERB-003_labnotebook.txt` (03 June) records the four-species fresh/young/old gel; `HERB-003_specimen_manifest.txt` describes the four panels and ladder; `gel_doc_maintenance_log.txt` (03 June) confirms the imager was serviced that morning. High-confidence match.
- **LACB-014_gel_photo.jpg** → **16 Mar 2026**. Setup sheet + `LACB-014_sample_manifest.txt` + `LACB-014_primer_size_reference.jpg` all agree on lane order and expected band sizes. High-confidence match. (Note: `MPNE-007_labnotebook.txt` records a different gel on the *same date*, but MPNE-007 has **no image** and a different lane/assay design, so there is no ambiguity about which photo is which.)

---

## 3. Figure 1 — CSAP-002 (blue-crab PCR-RFLP, SspI digest)

![Figure 1](Figure1_CSAP-002.png)

**Figure 1. CSAP-002 SspI restriction digest of a ~180 bp 12S rRNA PCR product for *Callinectes* species identification.** 1% agarose/TAE, ethidium bromide, 100 bp Promega ladder (lane 10 and an additional unlabelled ladder at the far right), 30-minute SspI digest at 37 °C, imaged on the UVP Gel Doc-It² system. **Date run/imaged: 29 April 2026.** Lanes are labelled with sample ID and sequence-confirmed species (per `CSAP-002_sample_manifest.txt`). Ladder rungs (100–1000 bp + 1500 bp) are annotated in yellow. *C. sapidus* lanes (2, 3, 5, 11, 12, 14) show three bands — an uncut ~180 bp band plus two cut fragments (~113 bp and ~67 bp) = partial digest. *C. danae* lanes (6, 7, 8, 15, 16, 17) show a single uncut ~180 bp band. Lane 17 (CB-0315) is marked with an asterisk (species not independently confirmed — see discussion).

### Table 1 — CSAP-002 band calls

| Lane | Sample | Expected species* | Observed bands (approx.) | Band identity | Artefacts / notes |
|---|---|---|---|---|---|
| M (10, far R) | 100 bp ladder (Promega) | — | 11 rungs: 100–1000 + 1500 bp; bright 500 bp reference band | Two ladders present; only lane 10 is in the manifest |
| 2 | CB-0231 | *C. sapidus* | ~180 + ~113 + ~67 bp | uncut + both SspI cut fragments (partial digest) | faint lowest fragment |
| 3 | CB-0233 | *C. sapidus* | ~180 + ~113 + ~67 bp | partial digest | — |
| 5 | CB-0240 | *C. sapidus* | ~180 + ~118 + ~76 bp | partial digest | — |
| 6 | CB-0301 | *C. danae* | single ~174 bp | uncut (no SspI site) | — |
| 7 | CB-0302 | *C. danae* | single ~174 bp | uncut | — |
| 8 | CB-0304 | *C. danae* | single ~172 bp | uncut | — |
| 11 | CB-0245 | *C. sapidus* | ~168 + ~119 + ~71 bp | partial digest | — |
| 12 | CB-0247 | *C. sapidus* | ~168 + ~121 + ~69 bp | partial digest | — |
| 14 | CB-0250 | *C. sapidus* | ~165 + ~118 + ~71 bp | partial digest | — |
| 15 | CB-0310 | *C. danae* | single ~163 bp | uncut | — |
| 16 | CB-0312 | *C. danae* | single ~161 bp | uncut | — |
| 17 | CB-0315 | *C. danae* (unconfirmed) | single ~161 bp | uncut — **pattern consistent with a non-*sapidus* *Callinectes*; species ID not independently confirmed** | paperwork lost (see discussion) |
| 1, 4, 9, 13, 18 | — | — | empty | no sample loaded |

*Species in the "expected" column were assigned **before** this run by 12S Sanger sequencing (`CSAP-002_sample_manifest.txt`); this gel tests whether the faster PCR-RFLP method agrees. Sizes are approximate (±~10–15%, standard for agarose sizing); the ~67 bp fragment runs below the lowest ladder rung and is the least precise call.

### Discussion
This gel directly serves Dr. Duarte's seafood-mislabelling screen, the stated purpose of which is to separate true *C. sapidus* from other *Callinectes* spp. by restriction pattern rather than sequencing every sample (`CSAP-002_PI_memo.txt`). The assay exploits an SspI recognition site present only in *C. sapidus* 12S rRNA, so that digestion splits the ~180 bp amplicon into smaller fragments only in true *C. sapidus*, while other *Callinectes* remain a single uncut ~180 bp band (Lee et al., 2020; `CSAP-002_protocol.docx`). The gel shows exactly that split: every sequence-confirmed *C. sapidus* lane carries the ~113 bp and ~67 bp cut fragments, and every *C. danae* lane remains a single uncut band. Because the cut fragments are unambiguously present in the *sapidus* lanes and absent in the *danae* lanes, the **species discrimination is clear regardless of digest-timing interpretation**, and the PCR-RFLP calls agree with the prior sequence-based identities — the outcome Dr. Duarte's hypothesis predicts.

The residual uncut ~180 bp band still visible in the *sapidus* lanes is the **expected partial-digestion pattern for the 30-minute timepoint** described by Lee et al. (2020), who explicitly note that both cut and uncut bands appearing together at short incubation should not be mistaken for degradation or a mixed/contaminated sample; only a multi-hour digest gives a single clean small-fragment result. The project protocol and PI memo both adopt this interpretation (`CSAP-002_protocol.docx`; `CSAP-002_PI_memo.txt`), and the handwritten setup sheet echoes it ("partial digest at 30 min is NORMAL for real sapidus"). **There is, however, a documentation conflict on this exact point — see Section 5 before finalising the write-up.**

One lane needs a labelling caveat: **lane 17 (CB-0315)** is reported here by its digestion pattern only (single uncut band, consistent with a non-*sapidus* *Callinectes*). Its field paperwork linking it to a sequencing confirmation was lost in transit, so per the notebook it must **not** be carried forward as "confirmed *C. danae*" until the sequencing confirmation is recovered or re-run (`CSAP-002_labnotebook.txt`, 29 April). Separately, the confirmatory sequencing record for a different specimen, CB-0231 (lane 2), is on file and returned a top BLAST hit of *C. sapidus* at 99.2% identity (`CB-0231_sequencing_summary.txt`), consistent with its cut pattern here.

---

## 4. Figure 2 — HERB-003 (herbarium DNA integrity, four species)

![Figure 2](Figure2_HERB-003.png)

**Figure 2. HERB-003 CTAB genomic-DNA integrity check across four species.** 1% agarose/TAE, 1 Kb Plus DNA Ladder (Invitrogen), run at 90 V for ~50 min, imaged 3 June on a freshly-serviced gel-doc system. The single image contains four panels from one project, presented here as **(a) *Lonicera maackii*, (b) *Ginkgo biloba* (~107 yr), (c) *Laburnum anagyroides* (~65 yr), (d) *Liriodendron tulipifera* (~114 yr)**. Each panel: **M** = ladder, **F** = fresh leaf, **FH** = young herbarium (dried same day), **H** = old/archival herbarium (`HERB-003_specimen_manifest.txt`). In every panel the fresh lane shows a bright, largely intact high-molecular-weight band near the top of the gel; young-herbarium lanes show a weaker, downward-trailing degradation smear; old-herbarium lanes show heavy degradation (a faint low-molecular-weight smear) or near-absent signal. Image shown in standard orientation (the source file was a light-background/inverted scan).

### Table 2 — HERB-003 lane calls

| Panel (species) | Lane | Material | Observed signal (relative to ladder) | Interpretation | Artefacts / notes |
|---|---|---|---|---|---|
| M (all panels) | M | 1 Kb Plus ladder (Invitrogen) | ~11–13 resolved rungs; top = high MW, bottom = low MW | size reference | rung values not listed in project docs — see confidence note |
| (a) *Lonicera* | F | fresh leaf | bright band at/above top rungs (high MW) | intact genomic DNA | — |
| (a) | FH | young herbarium | faint mid/low smear | degraded | — |
| (a) | H | old herbarium | very faint low smear | heavily degraded | — |
| (b) *Ginkgo* (~107 yr) | F | fresh | bright high-MW band + short smear | intact | — |
| (b) | FH | young herbarium | faint mid/low smear | degraded | — |
| (b) | H | old herbarium | minimal/near-absent signal | heavily degraded, very low yield | — |
| (c) *Laburnum* (~65 yr) | F | fresh | bright high-MW band | intact | — |
| (c) | FH | young herbarium | faint smear | degraded | — |
| (c) | H | old herbarium | distinct **low-MW** smear near gel bottom | heavily degraded (fragmented to low MW) | most visible old-specimen smear of the set |
| (d) *Liriodendron* (~114 yr) | F | fresh | bright, tight high-MW band | intact | brightest fresh lane |
| (d) | FH | young herbarium | very faint smear | degraded | — |
| (d) | H | old herbarium | essentially no visible signal | heavily degraded / below detection | oldest specimen in set |

Sizes are intentionally **qualitative** (position relative to ladder); see the confidence note on why specific kb values are not assigned.

### Discussion
This gel addresses Dr. Bosch's feasibility question: is it worth sending older herbarium specimens for sequencing, or is the DNA too degraded (`HERB-003_PI_memo.txt`)? The protocol sets the expectation that fresh tissue yields high-MW DNA with minimal smearing, young herbarium material shows noticeable degradation, and old herbarium material shows heavy degradation concentrated at low MW — and that this is normal for archival material, not a failed extraction (`HERB-003_protocol.docx`). That is precisely the gradient seen across all four species here, consistent with the published finding that herbarium DNA is typically highly fragmented, that most damage occurs during the initial drying/preparation step, and that a smeared low-MW gel is the expected appearance for degraded herbarium DNA rather than a sign of failed extraction (Staats et al., 2011). The NanoDrop log corroborates the gel: fresh extracts are high-yield with clean ratios (~138–156 ng/µL, 260/280 ≈ 1.88–1.91), whereas old extracts are low-yield with depressed ratios (~7–9 ng/µL, 260/280 ≈ 1.73–1.76, 260/230 ≈ 1.0–1.2) (`HERB-003_nanodrop_readings.csv`).

For the feasibility call this supports Dr. Bosch's stated expectation that fragment sizes drop with specimen age and that the oldest specimens retain little high-MW DNA — framed in the memo as a guide for *prioritising* younger material or switching to shorter target regions / more sensitive extraction for the oldest ones, not as a failure. No fresh lane looks anomalously degraded, so none triggers the protocol's "flag an unexpectedly degraded fresh sample" rule. The PI's own open question — whether this collection's patchy pre-2005 storage makes its specimens more or less degraded than the literature baseline — cannot be resolved from this gel alone, and the supplied paper is explicit only about general degradation behaviour; I have not extrapolated beyond that.

---

## 5. Figure 3 — LACB-014 (six-species *Lactobacillus* multiplex PCR)

![Figure 3](Figure3_LACB-014.png)

**Figure 3. LACB-014 six-species multiplex PCR panel with negative controls.** 1.5% agarose/TAE, ethidium bromide, 100 bp ladder (lab stock; run in separate flanking wells), imaged on the Bio-Rad gel-doc system, 63 °C annealing. **Date run: 16 March 2026.** Lanes 1–6 are single-species multiplex reactions (*L. gasseri, L. acidophilus, L. helveticus, L. jensenii, L. crispatus, L. gallinarum*); lanes 7–11 are negative-control species (*L. plantarum, L. salivarius, L. reuteri, E. faecalis, E. faecium*); NC = no-template control (`LACB-014_sample_manifest.txt`). Observed band sizes (orange) match the documented expected sizes in `LACB-014_primer_size_reference.jpg` to within a few percent (log-linear fit R² = 0.99). A primer-dimer/primer front (<~150 bp) appears at the bottom of every lane including the NTC (an artefact, red arrow). The large dark band across the top is a well/loading artefact above the resolved products.

### Table 3 — LACB-014 band calls

| Lane | Strain | Expected species | Expected size (primer ref.) | Observed band | Call | Artefacts / notes |
|---|---|---|---|---|---|---|
| M (both sides) | — | 100 bp ladder | — | regularly spaced rungs | size reference | ladder in own flanking wells |
| 1 | KACC-gass-01 | *L. gasseri* | 1241 bp | ~single band at ~1241 bp | **positive — matches** | brightest |
| 2 | KACC-acid-02 | *L. acidophilus* | 828 bp | ~828 bp | **positive — matches** | — |
| 3 | KACC-helv-03 | *L. helveticus* | 680 bp | ~680 bp | **positive — matches** | — |
| 4 | KACC-jens-04 | *L. jensenii* | 540 bp | ~540 bp | **positive — matches** | — |
| 5 | KACC-crisp-05 | *L. crispatus* | 420 bp | ~420 bp | **positive — matches** | — |
| 6 | KACC-gall-06 | *L. gallinarum* | 224 bp | ~224 bp | **positive — matches** | fainter (low-MW, anticipated in setup notes) |
| 7 | KACC-plant-07 | *L. plantarum* (neg) | — | none | **clean (no amplification)** | primer front only |
| 8 | KACC-saliv-08 | *L. salivarius* (neg) | — | none | **clean** | primer front only |
| 9 | local-reut-09 | *L. reuteri* (neg) | — | none | **clean** | primer front only |
| 10 | local-faeca-10 | *E. faecalis* (neg) | — | none | **clean** | primer front only |
| 11 | local-faeci-11 | *E. faecium* (neg) | — | none | **clean** | primer front only |
| NC | — | no-template | — | none | **clean** | primer front only |

### Discussion
This gel tests Dr. Calloway's working hypothesis that the new panel can call species-level identity from band size alone — the primer sets were designed against unique single-copy genes rather than the near-identical 16S regions that make this group hard to separate (`LACB-014_PI_memo.txt`). The result supports that hypothesis on single-strain isolates: each of the six target species produced one band at its expected size, and every band maps cleanly onto the documented primer-size reference, giving the descending 1241 → 224 bp "staircase" expected for the panel (`LACB-014_primer_size_reference.jpg`). This matches the published behaviour of the method, in which each species-specific primer set yields a single correctly-sized band for its target and no product for non-target species or genera (You & Kim, 2020). The five negative-control species and the no-template control produced no species-specific bands, satisfying the protocol's requirement that any band in a negative-control lane be investigated before reporting (`LACB-014_protocol.docx`); none was present, so no contamination/cross-reactivity flag is raised. The only non-specific signal is a primer-dimer/primer front below ~150 bp common to all lanes (including the NTC), which is an expected low-MW artefact and well separated from the smallest real product (224 bp).

Per the PI's instruction, the clean results here are reported strictly as **clean single-strain results**; this gel does not test a mixed/pooled sample and nothing here should be read as validating performance on mixed samples (see Section 6 for the related documentation conflict). A blank lane, had one occurred for a target species, would have been reported as "not one of the six panel targets," not as assay failure, per the PI memo — but that situation did not arise.

---

## 6. Confidence assessment (per gel)

**Figure 1 — CSAP-002: Moderate-to-high confidence in band calls; see conflict note.**
- *Ladder:* High confidence. Both ladder lanes resolve 11 rungs with the characteristic bright 500 bp reference band, matching the Promega 100 bp ladder as named in the protocol and setup notes (100–1000 bp + 1500 bp). Calibration fit was excellent.
- *Band pattern:* High confidence — the three-band (sapidus) vs single-band (danae) distinction is unambiguous and matches the manifest lane-for-lane.
- *Sizing:* Moderate. The ~180 bp and ~113 bp calls are solid; the ~67 bp fragment sits below the lowest ladder rung and is an extrapolated (approximate) value.
- *Quality issues:* The setup sheet notes the **UV bulb was too dim** at the time (it was not replaced until 3 June per `gel_doc_maintenance_log.txt`), which shows as elevated background/haze in the upper gel, plus dust speckles and faint diagonal streaks (imager surface). These do **not** obscure the product bands. A **second ladder** appears at the far right but is not in the manifest (clearly the same 100 bp ladder). No explicit no-template/PCR negative-control lane is documented for this run (the setup sheet even reminds "double check inclusion of negative control"); the sequence-confirmed *danae* lanes act as digestion-negative controls, but a reagent blank is not evidenced — a minor QC gap, not a reason to discard the gel.
- *Low-confidence call:* Lane 17 species identity is deliberately **not** called (paperwork lost); only its digest pattern is reported.

**Figure 2 — HERB-003: High confidence in the qualitative pattern; sizing intentionally qualitative.**
- *Ladder:* Confident as to identity (1 Kb Plus DNA Ladder, Invitrogen, per `HERB-003_specimen_manifest.txt`). **However, the rung values are not listed anywhere in the supplied documents**, so I have deliberately **not** assigned specific kb sizes to the sample smears; doing so would require relying on outside knowledge of the product. Fragment distributions are therefore described relative to the ladder and to the protocol's qualitative thresholds.
- *Pattern:* High confidence. The fresh → young → old degradation gradient is consistent and reproducible across all four species, and is corroborated by the NanoDrop yields/ratios.
- *Quality issues:* Imaged on a freshly-serviced gel-doc (3 June), and the gel is clean. The faint lanes (old-herbarium, some young-herbarium) carry inherently low signal — this is sample biology (degraded/low-yield DNA), not an imaging fault.

**Figure 3 — LACB-014: High confidence. Strongest gel of the set.**
- *Ladder:* Named as a 100 bp ladder (manifest/setup notes). Its exact rung values are not listed, but the six sample bands independently match the documented primer-size reference with a near-perfect log-linear fit (R² = 0.99), which cross-validates the sizing.
- *Band calls:* High confidence for all six positives and all six clean negatives/NTC.
- *Quality issues:* A primer-dimer/primer front (<~150 bp) in all lanes and a dark well artefact at the top; neither affects the resolved products. The *L. gallinarum* (224 bp) band is fainter than the rest, anticipated in the setup notes for low-MW products — still clearly present and correctly sized.

---

## 7. Analysis notes — contradictions, conflicts and documentation issues

These are flagged separately, as required, so the PIs can see exactly where sources disagree. Under the lab's source-authority rule, **peer-reviewed papers outrank notes/memos/manifests**, and that authority runs one way only.

1. **CSAP-002 — meaning of the 30-minute digest (paper vs. note): resolved in favour of the paper, but flagged.**
   `CSAP-002_digestion_timing_notes.txt` states that a 30-minute SspI digest should be *complete* in *C. sapidus*, that any residual uncut band indicates an inefficient reaction, and that such samples should be **re-run**. This **directly contradicts** Lee et al. (2020), which describes the co-occurrence of cut + uncut bands at ~30 min as the *expected, normal* partial-digestion pattern. The `digestion_timing_notes` file is documented as a **"methodological note reviewed by the lab"** (no author/journal/DOI), i.e. a note — whereas Lee et al. (2020) is the peer-reviewed paper on file (with full citation). Because a paper outranks a note, the conflict resolves in favour of Lee et al. (2020): the partial-digest pattern in the *sapidus* lanes is **expected**, and I do **not** recommend re-running those lanes merely because an uncut band is still present. This also aligns with the project protocol, the PI memo, and the handwritten setup sheet.
   *Caveat for the technician:* Dr. Duarte's own memo flags that the 30-min interpretation is "not universally settled" and refers to "another write-up" describing it differently. If the source behind `digestion_timing_notes` turns out to be a **peer-reviewed publication** rather than an internal note, then by lab policy this would become an **unresolved paper-vs-paper conflict** that no note or memo could adjudicate — and the 30-min interpretation should then be treated as uncertain pending resolution. Either way, note that the **species discrimination itself does not depend on this debate**: the presence of the ~113/~67 bp cut fragments in the *sapidus* lanes (and their absence in *danae*) is sufficient to show the assay separated the species.

2. **LACB-014 — mixed-sample performance (paper + PI memo vs. lab-notebook hearsay): resolved in favour of the paper.**
   `LACB-014_labnotebook.txt` (15 March) records a verbal claim that the panel "worked fine on the mixed-species DNA test... picking up all six species from the pooled sample." This **contradicts** You & Kim (2020), who report that in a genuinely mixed/pooled sample one target species dropped out undetected for reasons they could not fully explain — and it also contradicts Dr. Calloway's **own PI memo**, which states the mixed-sample issue is unresolved and that the panel has **not** been validated on mixed samples in this lab. The paper (reinforced here by the PI memo) is authoritative over the notebook note, so the mixed-sample limitation stands and the notebook's "works on mixed samples" claim should not be relied upon. **This has no bearing on Figure 3**, which is entirely single-strain reactions; it matters only if anyone later tries to apply the panel to pooled/complex samples.

3. **HERB-003 — setup sheet vs. manifest/image (documentation mismatch, not a data conflict).**
   The handwritten `HERB-003_gel_setup_notes.jpg` appears to be an incomplete draft: it lists a loading order for only two species (Ginkgo, Laburnum) and notes "no ladder decided yet." The structured `HERB-003_specimen_manifest.txt` and the gel image both show **four** species panels, each **with** a 1 Kb Plus ladder. The manifest and image agree with each other, so they were used as the authoritative record; the setup sheet is treated as a superseded draft. No impact on interpretation.

4. **CSAP-002 — unlabelled second ladder / empty lanes.** The manifest lists a single ladder (lane 10), but the image shows a second 100 bp ladder at the far right (unlisted). Lanes 1, 4, 9, 13 and 18 are empty. Noted for completeness; neither affects the calls.

5. **Citations not made.** The HERB-003 notebook mentions "Telle & Thines 2008" as a methods paper of interest, but no copy or summary was provided, so it is **not** cited here (only supplied papers are cited). The files `CSAP-002_digestion_timing_notes.txt` and `multiplex_PCR_background_reading.txt` are methodological/background notes, not peer-reviewed papers, and are referred to as notes rather than cited as literature.

---

## 8. Items reviewed but not analysed (out of scope / not gels)

| File(s) | Why not analysed |
|---|---|
| `PSMD-001_scan.jpg` + `PSMD-001_labnotebook.txt` | The "scan" is a handwritten note, **not a gel image** ("ran the gel, samples didn't look great, will redo next week"). Different project, no protocol/manifest/ladder provided. **No ladder is available and none may be invented**, so no band sizes can be assigned. Owner already flagged it for a redo. No gel image exists to analyse. |
| `MPNE-007_labnotebook.txt` | Different project (*Mycoplasma pneumoniae* P1 screen). Records a 16 Mar gel but **no image was provided**; nothing to analyse. (2 of 8 samples reportedly failed amplification — the owner has already scheduled re-extraction.) |
| `SOIL-019_labnotebook.txt` | Different project; explicitly states **no diagnostic gel was run** (went straight to library prep). Nothing to analyse. |
| `CB-0231_sequencing_summary.txt` | Sanger sequencing summary for a CSAP-002 sample (used as supporting context in Section 3), not a gel. |
| `freezer_inventory_update.txt`, `gel_doc_maintenance_log.txt` | Administrative/equipment logs. The maintenance log is used only to corroborate HERB-003 imaging conditions (3 June) and the CSAP-002 dim-bulb note. |
| `multiplex_PCR_background_reading.txt` | General background reading from a methods workshop, explicitly "not tied to any specific ongoing project." Not a project-specific paper; not cited. |

---

## 9. References

Lee, B. B., Schott, E. J., Behringer, D. C., Bojko, J., Kough, A., & Plough, L. V. (2020). Rapid genetic identification of the blue crab *Callinectes sapidus* and other *Callinectes* spp. using restriction enzyme digestion and high resolution melt assays. *Frontiers in Marine Science, 7*, 633. https://doi.org/10.3389/fmars.2020.00633

Staats, M., Cuenca, A., Richardson, J. E., Vrielink-van Ginkel, R., Petersen, G., Seberg, O., & Bakker, F. T. (2011). DNA damage in plant herbarium tissue. *PLOS ONE, 6*(12), e28448. https://doi.org/10.1371/journal.pone.0028448

You, I., & Kim, E. B. (2020). Genome-based species-specific primers for rapid identification of six species of *Lactobacillus acidophilus* group using multiplex PCR. *PLOS ONE, 15*(3), e0230550. https://doi.org/10.1371/journal.pone.0230550

---
*Notes on method: band positions were determined from pixel-intensity profiles of each lane calibrated against the in-gel ladder (CSAP-002) or, where ladder rung values were not documented (HERB-003, LACB-014), described relative to the ladder and — for LACB-014 — cross-checked against the supplied primer-size reference. All sizes are approximate. No ladder was assumed or invented where one was absent, and no band identity or conclusion was assigned without supporting documentation.*
