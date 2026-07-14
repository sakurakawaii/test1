# May 2026 SLA reporting rules

Use this file as the source of truth for the May 2026 service desk SLA report.

## Files

The report has three data inputs:

- `ticket_export_may2026.csv` — raw ticket-level export from the service desk system
- `customer_lookup_may2026.csv` — authoritative customer tier lookup for May 2026
- `draft_management_summary.md` — draft narrative to review against the data and rules

The `CRM_Tier_Snapshot` column in the ticket export is not authoritative for SLA reporting. It is a CRM snapshot taken at ticket creation and may be stale or blank. For priority rules that depend on customer tier, join tickets to `customer_lookup_may2026.csv` using `Account_ID` and use `SLA_Customer_Tier`.

If an in-scope ticket's `Account_ID` is missing from the lookup, keep the ticket in scope, flag it as a data-quality issue, and only use `CRM_Tier_Snapshot` as a fallback for that ticket.

## Scope

Include tickets opened from **2026-05-01 00:00 UTC through 2026-05-31 23:59 UTC**.

Exclude a ticket from SLA attainment if any of the following apply:

- `Internal_Test` is `TRUE`
- `Duplicate_Of` is populated
- `Cancelled` is `TRUE`
- `Category` is `Password Reset` because these are handled through self-service identity tooling

Do not exclude tickets just because they were resolved quickly or because they were opened outside normal office hours.

## Response timestamp to use

For SLA attainment, use `Meaningful_Response_At_UTC`.

Do **not** use `First_Response_At_UTC` when `First_Response_Type` is `Auto acknowledgement`. Automated acknowledgements are only receipt confirmations and do not count as a meaningful analyst response.

If `Meaningful_Response_At_UTC` is blank for an in-scope ticket, count the ticket as a breach.

## Effective priority

Calculate SLA against the effective priority, not always the reported priority. Never downgrade a ticket; use the highest urgency produced by the rules below.

A ticket is effective **P1** if any of these are true:

- `Reported_Priority` is `P1`
- `Category` is `Major Outage`
- `Impacted_Users` is 25 or more

A ticket is effective **P2** if it is not already effective P1 and any of these are true:

- `Reported_Priority` is `P2`
- `Category` is `Data Issue` and `Impacted_Users` is 5 or more
- linked `SLA_Customer_Tier` from `customer_lookup_may2026.csv` is `Gold` and `Impacted_Users` is 10 or more

Otherwise, use the reported priority.

## First meaningful response SLA thresholds

Measure elapsed calendar minutes from `Opened_At_UTC` to `Meaningful_Response_At_UTC`.

| Effective priority | SLA threshold |
|---|---:|
| P1 | 15 minutes |
| P2 | 60 minutes |
| P3 | 240 minutes |
| P4 | 720 minutes |

A response exactly at the threshold counts as met.

## Management reporting expectations

The monthly summary should include:

- the corrected in-scope ticket count
- SLA attainment as met tickets / in-scope tickets
- breach count by effective priority
- notable data-quality or process issues
- whether any effective P1 ticket was missing a `Major_Incident_Declared = TRUE` flag
- any customer-tier lookup mismatches or stale CRM tier snapshots that affected priority classification
