# Service Desk SLA Report — May 2026

*Prepared for internal management review. Figures recomputed from the raw ticket export against the May 2026 SLA reporting rules; they supersede the earlier draft summary.*

---

## Headline figures

| Metric | Value |
|---|---:|
| In-scope tickets | **43** |
| SLA met | 34 |
| SLA breached | **9** |
| **SLA attainment** | **79.1%** |
| Effective P1 incidents | **3** |
| P1 incidents missing a major-incident flag | **1** |

> **Bottom line:** May attainment was **79.1%**, not the 96% stated in the draft. Nine tickets breached, not two. Breaches concentrate in BI & Reporting and disproportionately affect Gold-tier customers, and one effective-P1 finance outage both breached its 15-minute target and was never declared as a major incident. This needs management attention rather than "no action required."

---

## Management summary

May service desk performance was weaker than the draft indicated. Against the SLA rules, **34 of 43 in-scope tickets met their first-meaningful-response target (79.1%)**. The nine breaches were spread across five service areas but clustered in **BI & Reporting (4 of 9)** and hit **Gold-tier customers in 6 of 9 cases**.

The single most serious issue is **TCK-1024** — a Finance Systems outage affecting 42 users for Gold customer Harbour Finance Group. It was logged as P2 but qualifies as an **effective P1** (Major Outage and ≥25 users). It breached the 15-minute P1 target (27 minutes to meaningful response) **and no major incident was declared**, which is a process/governance gap, not just an SLA miss.

A recurring pattern sits underneath several breaches: tickets reported as **P3 that are actually effective P2** (Data Issues affecting ≥5 users, or Gold customers with ≥10 impacted users). These were worked at a P3 pace and missed the tighter 60-minute P2 target. This is a triage/classification problem that is being masked by stale CRM tier data.

The draft's "≈2-minute average first response" is misleading: it measures the **automated acknowledgement**, which the rules explicitly exclude. Measured on genuine analyst (meaningful) responses, median times were ~14 min (P1), ~56 min (P2), ~165 min (P3) and ~500 min (P4) — materially different from the impression the draft gives.

### Suggested message for leadership

> May SLA attainment was 79.1% (34 of 43 in-scope tickets), below target, with nine breaches concentrated in BI & Reporting and affecting Gold-tier customers in most cases. One Finance Systems outage qualified as an effective P1, breached its response target, and was not declared as a major incident — we are reviewing that specifically. A recurring pattern of P3-logged tickets that should have been triaged as P2, combined with stale CRM tier data, is contributing to misses. We recommend a triage/classification review and a fix to the tier-lookup process rather than treating May as business-as-usual.

---

## Breach detail

All nine in-scope breaches, measured from `Opened_At_UTC` to `Meaningful_Response_At_UTC` against the effective-priority threshold.

| Ticket | Customer (tier) | Service area | Reported → Effective | Response vs target | Why it breached |
|---|---|---|---|---|---|
| **TCK-1024** | Harbour Finance (Gold) | Finance Systems | P2 → **P1** | 27 min / 15 min | Major outage, 42 users; effective P1; **no major-incident flag** |
| TCK-1029 | Harbour Finance (Gold) | Corporate Apps | P2 → P2 | **no meaningful response logged** | Blank `Meaningful_Response_At_UTC` → counts as breach |
| TCK-1014 | Causeway Analytics (Gold) | BI & Reporting | P3 → **P2** | 200 min / 60 min | Gold + 11 users → effective P2; worked as P3 |
| TCK-1041 | Causeway Analytics (Gold) | Data Platform | P3 → **P2** | 95 min / 60 min | Data Issue, 9 users, Gold → effective P2 |
| TCK-1015 | Lagan Manufacturing (Silver) | Data Platform | P3 → **P2** | 72 min / 60 min | Data Issue, 5 users → effective P2 |
| TCK-1008 | Mourne HR Services (Std) | HR System | P2 → P2 | 80 min / 60 min | Missed P2 target |
| TCK-1019 | Foyle Utilities (Gold) | BI & Reporting | P3 → P3 | 300 min / 240 min | Missed P3 target |
| TCK-1033 | Foyle Utilities (Gold) | BI & Reporting | P3 → P3 | 280 min / 240 min | Late analyst assignment |
| TCK-1046 | Erne Logistics (Std) | BI & Reporting | P4 → P4 | 900 min / 720 min | Sat unassigned overnight |

### Breach themes

- **BI & Reporting is the biggest hotspot** — 4 of 9 breaches (TCK-1014, 1019, 1033, 1046), several from work sitting unassigned. The draft's instinct to watch this queue was right; it just understated the scale.
- **Gold customers bear the brunt** — 6 of 9 breaches hit Gold accounts (Harbour Finance, Causeway Analytics, Foyle Utilities), the tier where misses carry the most commercial and relationship risk.
- **Mis-triage of effective P2s** — TCK-1014, 1015 and 1041 were all logged P3 but are effective P2. They were handled at roughly P3 speed and missed the 60-minute target. This is a classification gap, not raw capacity.
- **Cross-area, not a single spike** — breaches span Finance, HR, Data Platform, Corporate Apps and BI & Reporting, so the draft's "unusually high analyst workload in the reporting queue" is only a partial explanation.

---

## Effective-priority note

Effective priority was calculated per the rules (never downgraded; highest applicable urgency used). Seven in-scope tickets carry an effective priority higher than reported:

- **P3 → P1:** TCK-1037 (Major Outage, 28 users) — met target; major incident correctly declared.
- **P2 → P1:** TCK-1024 (Major Outage, 42 users) — breached; major incident **not** declared.
- **P3 → P2:** TCK-1010, TCK-1014, TCK-1015, TCK-1032, TCK-1041 (Data Issues ≥5 users, or Gold + ≥10 users).

There were **3 effective P1 incidents** in May (TCK-1003, TCK-1024, TCK-1037), directly contradicting the draft's "no P1 incidents." TCK-1003 and TCK-1037 met target with major incidents declared; **TCK-1024 is the outlier** on both counts.

---

## Data-quality concerns and assumptions

1. **Stale CRM tier snapshots (8 in-scope tickets).** `CRM_Tier_Snapshot` read "Standard" for 8 tickets whose authoritative tier (from `customer_lookup_may2026.csv`) is Gold or Silver. Per the rules, the authoritative lookup was used. Had the CRM snapshot been relied on, several Gold/Silver tickets would have been under-classified and their breaches hidden — this is the root cause behind the mis-triaged effective P2s and should be fixed at source.

2. **Misleading analyst note — TCK-1022.** The note calls this a "Gold customer with 12 impacted users; effective P2," but the authoritative lookup shows the account (Mourne HR Services, ACC-210) is **Standard**. Under the rules it is correctly **effective P3** and it met target. Flagged because notes/snapshots should not drive classification — the lookup is the source of truth. No numbers change.

3. **Missing meaningful response — TCK-1029.** A Gold-customer P2 has a blank `Meaningful_Response_At_UTC`. Per the rules this counts as a breach. It should be confirmed whether this is a genuine no-response or a logging gap; either way it is a data-integrity issue worth chasing.

4. **Auto-acknowledgement metric is not a performance measure.** The draft's ~2-minute "average first response" is the automated receipt confirmation, which the rules exclude from SLA. It should not be reported to leadership as responsiveness.

5. **Account lookup coverage — no gaps.** Every in-scope ticket's `Account_ID` was present in the customer lookup, so no CRM-snapshot fallback was needed. (ACC-250 / Internal IT appears only on excluded tickets.)

### Scope and exclusions (8 tickets excluded)

| Reason | Tickets |
|---|---|
| Password Reset (self-service) | TCK-1043, TCK-1048 |
| Internal test | TCK-1044, TCK-1049 |
| Duplicate of another ticket | TCK-1045 (→1027), TCK-1050 (→1008) |
| Cancelled | TCK-1047, TCK-1051 |

Note: **TCK-1049** looks like a severe P1 (Major Outage, 99 users) but is a flagged disaster-recovery **internal test**, correctly excluded rather than counted as a real P1 incident.

---

## Recommended actions

1. **Post-incident review of TCK-1024** — why a 42-user finance outage was logged P2 and never declared a major incident, and close the response-time gap.
2. **Fix the CRM tier-snapshot feed** so ticket classification reflects the authoritative customer tier at triage time.
3. **Triage refresh on effective-P2 rules** (Data Issue ≥5 users; Gold + ≥10 users) so these stop being worked as P3.
4. **Investigate TCK-1029's missing response record** and add a control for blank meaningful-response timestamps.
5. **Reduce unassigned dwell time in BI & Reporting**, the queue behind most breaches.

---

*Sources: `ticket_export_may2026.csv`, `customer_lookup_may2026.csv`, `sla_rules.md`. Attainment = met ÷ in-scope. Priorities and thresholds applied exactly as defined in the rules file.*
