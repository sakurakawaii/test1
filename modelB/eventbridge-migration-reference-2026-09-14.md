# EventBridge Migration Reference — Consolidated Engineering Guidance

**Date:** 2026-09-14
**Primary authority:** Priya Nair, "EventBridge cutover — consolidated status and confirmed decisions" (email, 2026-09-14, 08:47) — stated by Platform Engineering as the current authoritative position
**Secondary sources:** EventBridge API Spec v2.0.1 (Approved), Release Notes v2.1.0 (Final), Webhook Delivery SLA v1.0 (Approved), Migration Policy v2.0 (Approved, effective 2026-09-01), Technical Quick Reference (2026-08-20), migration tracker (2026-07-01), engineering sync notes (Aug 5 / Aug 18 / Sep 10), email threads, #platform-eng Slack export (2026-09-12), support ticket summary (2026-09-08)
**Intended use:** Single actionable reference for engineering leads and implementing teams for the final migration sprint. Values below are definitive unless explicitly marked as derived.

---

<summary>

**Five decisions are now closed per Priya Nair's 2026-09-14 update and should be treated as final:**

1. **DLQ threshold is 3 total delivery attempts.** The v2.0.1 spec's "5 consecutive failed delivery attempts" was a documentation error. Build retry logic and alerting around 3.
2. **Rate limit: 1200 events/min becomes the permanent default on 2026-11-01** (VP sign-off received 2026-09-12). The 2027-01-01 reversion to 1000/min described in the v2.1 release notes and v2.0.1 spec no longer applies. Until 2026-11-01, the live default remains 1000/min, with 1200/min available on request.
3. **Partner Notification Feed is Deprecated effective 2026-09-15**, which triggers the accelerated sunset date of **2026-11-30** under Migration Policy v2.0 §2.
4. **Analytics Dashboard has a hard internal migration deadline of 2026-11-15.**
5. **LogArchive exception is formally approved**, covering LogArchive **and services with a direct runtime dependency on the LogArchive storage pipeline**; these are exempt from the 2026-12-31 deadline pending the storage backend migration (Q1 2027 at earliest).

**Four migrations are confirmed complete with Platform Engineering sign-off issued 2026-09-14:** CS Tooling, Billing Sync, Fraud Detection, Payment Gateway Webhooks.

**Where Priya's update is silent, the following calls are made in this document** (evidence in the Analysis section): delivery signature header is `X-EventBridge-Signature`; subscription registration path is `POST /subscriptions` (not `/v2/subscriptions`, not `/webhooks/register`); OAuth2 token endpoint is `https://auth.pitaron.io/oauth/token`; minimum secret length is 32 characters.

</summary>

---

<analysis>

## Conflict register — how each contested value was resolved

| # | Item | Conflicting sources | Resolution | Basis |
|---|---|---|---|---|
| 1 | DLQ threshold | Spec v2.0.1 says **5** (and asserts "the correct threshold has always been 5"); Release Notes v2.1 and SLA v1.0 say **3**; Slack/support guidance through August said "use 5 as working assumption"; a wiki cited "4"; gateway config extract (Nadia Osei, 2026-09-12) shows `delivery_retry_max_attempts = 3` with ambiguous retries-vs-total semantics | **3 total delivery attempts** | Priya 2026-09-14, closing the Tariq Bashir escalation: live gateway enforces 3; spec's "5" was a drafting error; the retries-vs-total question is a config parameter naming convention, not a behavioural difference — effective threshold is 3 **total** attempts. All pre-Sep-14 "use 5" guidance is superseded. |
| 2 | Rate limit | Spec v2.0.1 and Release Notes v2.1: default 1000/min, 1200/min temporary through 2026-12-31, reverting 2027-01-01; James Okafor's 2026-09-03 "permanent 1200" email was walked back at the 2026-09-10 sync as premature (VP sign-off outstanding) | **1200/min permanent default from 2026-11-01; no reversion on 2027-01-01** | Priya 2026-09-14: capacity review complete, VP sign-off received 2026-09-12. James's 2026-09-03 practical guidance is reinstated as accurate. Spec/release-notes update pending (owner: James). |
| 3 | Delivery signature header | SLA v1.0 §3 names `X-PiSync-Signature` as the compliance header; draft migration guide (May) also says `X-PiSync-Signature`; Release Notes v2.1 left the name unconfirmed; a document in circulation uses `X-EventBridge-Sig` | **`X-EventBridge-Signature`** | Priya silent — call made. Spec v2.0.1 (Approved, newer than the SLA) is explicit, and explicitly warns against `X-PiSync-Signature`; quick reference, archived PiSync spec mapping table, and 8 resolved support tickets all corroborate. The SLA v1.0 header name is an error (published 2026-06-15, pre-dating the spec clarification). `X-EventBridge-Sig` is a known incorrect truncation (support ticket summary). |
| 4 | Registration endpoint path | Draft migration guide instructs `POST /webhooks/register` (legacy PiSync path); a claim in #engineering said the path is `/v2/subscriptions` | **`POST /subscriptions`** | James Okafor, Slack 2026-09-08: documented path is `/subscriptions`; staging 404s are a staging-environment issue, not a path change. Spec, SLA, and quick reference agree. Legacy endpoint rejects new registrations. |
| 5 | OAuth2 token endpoint | Quick reference: `https://auth.pitaron.internal/v1/oauth/token`; Spec v2.0.1 and draft guide: `https://auth.pitaron.io/oauth/token` | **`https://auth.pitaron.io/oauth/token`** | Priya silent — call made. The Approved spec is the canonical API document and two independent sources agree with it; the quick reference contains multiple demonstrated errors (see #6, #7), reducing its weight. |
| 6 | Minimum secret length | Quick reference: 16 chars; Spec and SLA: 32 chars (SLA adds max 256) | **Min 32 / max 256 characters** | Two Approved documents agree; quick reference is the outlier. |
| 7 | Retry schedule | Quick reference table shows "fixed 60 seconds" (its own footnote admits these are legacy PiSync values); spec defines exponential backoff | **Exponential backoff** (schedule below, marked derived) | Spec v2.0.1; PiSync's fixed 60s interval applies only to the legacy system. |
| 8 | Partner Notification Feed status | Tracker (2026-07-01): Maintenance; informal data-team email claimed Deprecated (unconfirmed at 2026-09-10 sync). Policy v2.0 requires written PE-lead confirmation to trigger the accelerated deadline | **Deprecated effective 2026-09-15; sunset 2026-11-30** | Priya's 2026-09-14 email constitutes the required written confirmation from the Platform Engineering lead. |
| 9 | LogArchive exception scope | Policy v2.0 §3: exceptions cover the named service only; dependent services must apply separately. Sep 10 sync conditioned approval on written scope by 2026-09-30 | **Exception covers LogArchive plus direct runtime dependents of the LogArchive storage pipeline** | Priya 2026-09-14: "I've approved this formally." A documented approved exception from the policy owner supersedes the policy default; preserved here as a final decision. |
| 10 | "November 1 soft cutoff" for migration | Three support tickets referenced a "November 1 soft cutoff"; Connor Marsh (2026-07-28) confirmed no such date was ever agreed | **No November 1 migration cutoff exists** | The only confirmed November dates are: 2026-11-01 (rate-limit baseline change), 2026-11-15 (Analytics internal deadline), 2026-11-30 (Deprecated-service sunset). General Sunset Date remains 2026-12-31. |
| 11 | Payment Gateway Webhooks status | Tracker: In Progress; completion report submitted 2026-08-28, support-closed 2026-08-30 but no PE verification (Policy §4: support closure ≠ verification) | **Complete, verified** | Priya 2026-09-14: PE sign-off issued. |
| 12 | Risk Alerts completion rumours | "Heard it was done last week" (Sep 10 sync); owner Marcus Webb could not confirm; two open tickets show intermittent signature failures consistent with partial legacy-path traffic | **In Progress — not complete** | Not in Priya's confirmed-complete list; Policy §4 bars treating unverified claims as Complete. |
| 13 | Billing Sync completion date | Aug 5 sync: "done as of last week"; tracker target Sep 2026; Sep 10 sync: "migrated and verified end of August" | **Verified end of August 2026** | Most recent sync record carries the verification statement; PE sign-off 2026-09-14. |

**Document reliability notes:**

- **Draft migration guide (Connor Marsh, May 2026):** Draft status, never published, flagged at the 2026-08-05 sync as superseded and containing errors. **Do not use.** Contains wrong registration path (Step 2), wrong signature header (Step 3), and its "3-attempt" figure in Step 4, while numerically matching the confirmed threshold, is justified by incorrect reasoning (carry-over from PiSync) with the wrong retry schedule.
- **Technical Quick Reference (2026-08-20):** Approved, but contains at least four errors (token endpoint, secret length, retry schedule, and a rate-limit table presenting 1200 as the current default before 2026-11-01). Use this document instead until it is corrected.
- **EventBridge API Spec v2.0.1:** Authoritative for endpoints, payloads, auth, and topics — but its DLQ section (threshold 5 and the note claiming "the correct threshold has always been 5") and rate-limit section (2027-01-01 reversion) are superseded by Priya's 2026-09-14 decisions. Updates pending (owner: James Okafor).
- **Webhook Delivery SLA v1.0:** Authoritative for latency/availability commitments, endpoint requirements, and the DLQ threshold (3) — except the signature header name, which is an error (see #3).
- **Archived PiSync v1 spec:** Historical reference only; valid here solely for the field-name mapping table and legacy behaviour comparison, which the v2 spec corroborates.
- **Migration tracker (2026-07-01):** Stale; superseded by the per-service table below.

</analysis>

---

<deliverable>

# Part 1 — Definitive Technical Configuration Values

## 1.1 Authentication (management API)

| Parameter | Value | Source |
|---|---|---|
| Method | OAuth2 client credentials only — API keys **not** supported on EventBridge | Spec v2.0.1 |
| Token endpoint | `POST https://auth.pitaron.io/oauth/token` | Spec v2.0.1 (see conflict #5) |
| Grant type | `client_credentials` | Spec v2.0.1 |
| Scopes | `eventbridge:read eventbridge:write` (`write` for create/delete; `read` for list/inspect) | Spec v2.0.1 / quick ref scope table |
| Token lifetime | 3600 seconds — refresh with **≥ 5-minute buffer** | Spec v2.0.1; Connor Marsh, 2026-07-28 |
| Client library | `pitaron-auth-client` v2.4+ (auto-refresh, JVM); non-JVM runtimes see OAuth2 onboarding guide on the Platform Eng wiki | Spec v2.0.1 |
| Credential provisioning | IAM portal | Draft guide / quick ref (consistent) |

## 1.2 Subscription management

| Operation | Method and path |
|---|---|
| Create subscription | `POST /subscriptions` |
| List subscriptions | `GET /subscriptions?service_id={id}` (optional filters: `topic`, `status` = active / paused / errored) |
| Get subscription | `GET /subscriptions/{subscription_id}` |
| Delete subscription | `DELETE /subscriptions/{subscription_id}` (in-flight deliveries complete; no new dispatch after acknowledgement) |
| Inspect DLQ | `GET /subscriptions/{subscription_id}/dlq` (cursor-paginated; required above 500 events per v2.1 fix) |

**Do not use** `POST /webhooks/register` (legacy PiSync — rejects new registrations) or `/v2/subscriptions` (incorrect rumour; James Okafor confirmed 2026-09-08 that the documented path is `/subscriptions`). Note: `POST /subscriptions` 404s reported in **staging** by three teams are a staging-environment defect under investigation — open a ticket, do not change the path.

| Constraint | Value |
|---|---|
| Max active subscriptions per service | 200 (`400 subscription_limit_exceeded` beyond) |
| Secret length | Min 32 / max 256 characters (quick ref's "16" is wrong) |
| Endpoint URL | HTTPS only, valid TLS cert, reachable from the EventBridge delivery network |
| Duplicate registration | `409 duplicate_subscription` on same service_id + topic + endpoint_url |
| Topic wildcards | Family-level only (e.g. `account.*`); global `*` not supported |

## 1.3 Delivery contract

| Parameter | Value |
|---|---|
| Delivery method | HTTP POST to registered `endpoint_url` |
| Success condition | **2xx within 10 seconds**; anything else (including timeout) counts as a delivery failure |
| Delivery guarantee | At-least-once — endpoints **must be idempotent** on `event_id` |
| 5xx semantics | Never return 5xx for business-logic/downstream errors after successful processing — it triggers retry and burns the DLQ threshold |
| Event shape | `event_id`, `topic`, `payload`, `timestamp`, `version: "2"` |
| Signature header | `X-EventBridge-Signature: sha256=<hex>` |
| Signature algorithm | HMAC-SHA256 of the **raw request body** using the subscription `secret` |

Known-wrong header names — reject these if found in code or docs: `X-PiSync-Signature` (legacy PiSync/shim deliveries only; appears in SLA v1.0 §3 in error and in the superseded draft guide) and `X-EventBridge-Sig` (truncated variant circulating in an unidentified internal document, per support tickets).

Reference validation (spec v2.0.1):

```python
import hmac, hashlib

def validate(body_bytes, secret, header_value):
    expected = "sha256=" + hmac.new(
        secret.encode(), body_bytes, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, header_value)

# header_value = request.headers["X-EventBridge-Signature"]
```

## 1.4 Retry policy and Dead Letter Queue — CONFIRMED 2026-09-14

| Parameter | Value |
|---|---|
| **DLQ threshold** | **3 total delivery attempts** (initial attempt + 2 retries), then the event moves to the DLQ |
| Live gateway parameter | `delivery_retry_max_attempts = 3` (ops config extract, 2026-09-12). Per Priya Nair / Tariq Bashir: the parameter name is a naming-convention artifact — **the effective behaviour is 3 total attempts**, not 3 retries after the initial attempt |
| Backoff | Exponential. Applicable schedule *(derived — see note)*: attempt 1 immediate → attempt 2 after 30 s → attempt 3 after 2 min → DLQ (≈ 2.5 min max from first attempt to DLQ) |
| DLQ retention | 14 days, then expiry — **escalate any DLQ event older than 13 days** (SLA) |
| Replay | Manual only via the DLQ endpoint; automated replay not available (roadmap item) |
| Alerting | Tune consumer alerting to the 3-attempt threshold. Any alerting or consumer logic built on the spec's "5" (or a wiki's "4") must be corrected **now** — events reach the DLQ far earlier than a 5-attempt assumption implies |

*Derived-value note:* the 30 s / 2 min delays are the first two backoff intervals from the spec v2.0.1 table, which was written for a 5-attempt regime; under the confirmed 3-attempt threshold the 10-min and 30-min rows are unreachable. No supplied document restates the schedule for the 3-attempt regime; the spec update is pending. The threshold itself (3) is confirmed, not derived.

The spec v2.0.1 DLQ section — including its note asserting "the correct threshold has always been 5" — is **superseded**. Release Notes v2.1 and SLA v1.0 were correct on this point.

## 1.5 Rate limits — CONFIRMED 2026-09-14 (VP sign-off 2026-09-12)

| Period | Default delivery limit | Notes |
|---|---|---|
| Now → 2026-10-31 | **1000 events/min** per subscription | 1200/min elevation available on request in #platform-eng for parallel-run services |
| From **2026-11-01** | **1200 events/min** per subscription — **permanent** | Applied automatically; no request needed. Services already holding the elevation keep it as their permanent baseline with no action |
| 2027-01-01 | No change | The reversion to 1000/min stated in the v2.1 release notes and v2.0.1 spec **will not happen** |

- New designs may treat **1200/min as the permanent capacity floor**; teams that capacity-planned for 1000/min should revise.
- Scope: **event delivery only.** The management API (including DLQ inspection) has its own separate limit, unaffected (James Okafor, 2026-09-03). Its numeric value is not stated in any supplied document — confirm in #platform-eng if you need it.
- Migration Policy v2.0 §5 (elevation expiring 2026-12-31, separate arrangement for exception services) is mooted by the permanent baseline: LogArchive-exception services receive the 1200/min default like everyone else from 2026-11-01.
- Headers on management calls: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## 1.6 Delivery SLA commitments (SLA v1.0, unchanged)

| Metric | Commitment |
|---|---|
| Delivery latency p50 / p99 | < 2 s / < 15 s from emission to first delivery attempt |
| Platform availability | 99.9% monthly uptime (excl. scheduled maintenance; ≥ 48 h notice via #platform-eng) |
| Incident escalation | #platform-eng; production incidents via Platform Engineering on-call (PagerDuty) |

## 1.7 Topics

`account.created`, `account.updated`, `account.status_changed` (accounts-svc) · `billing.invoice_issued`, `billing.payment_received` (billing-svc) · `risk.alert_raised` (risk-svc) · `partner.event` (partner-relay). Wildcards: family-level only. Known cosmetic issue: wildcard subscriptions list without sub-type filtering via `GET /subscriptions`; delivery behaviour is correct.

## 1.8 PiSync → EventBridge migration mapping

| PiSync (legacy) | EventBridge (current) |
|---|---|
| `POST https://pisync.pitaron.internal/webhooks/register` | `POST /subscriptions` on EventBridge |
| `X-Api-Key` header auth (`PISYNC_API_KEY`) | OAuth2 client credentials (§1.1) |
| `service_name` / `event_type` / `target_url` / `signing_secret` | `service_id` / `topic` / `endpoint_url` / `secret` |
| `webhook_id` | `subscription_id` |
| `X-PiSync-Signature` | `X-EventBridge-Signature` |
| 3 retries, fixed 60 s interval, internal dead-letter store | 3 total attempts, exponential backoff, per-subscription DLQ (14-day retention, manual replay) |
| 500 events/min default | 1000/min now; 1200/min permanent from 2026-11-01 |

**Migration completion requires all four** (Policy v2.0 §6): PiSync subscriptions deregistered/confirmed inactive → EventBridge subscriptions active and delivering → completion report submitted to Platform Engineering → **formal written PE verification issued**. Support-ticket closure does not count. Parallel running of PiSync (via the shim) and EventBridge is safe during cutover. Remove `PISYNC_API_KEY` from config after cutover.

---

# Part 2 — Per-Service Migration Status (authoritative as of 2026-09-14)

| Service | Owner team | Topics | Status | Completion / deadline | PE sign-off | Notes |
|---|---|---|---|---|---|---|
| CS Tooling | Customer Success Eng | account.updated, account.status_changed | **Complete** | Migrated June 2026 | **Issued 2026-09-14** | No issues reported |
| Billing Sync | Finance Eng | billing.invoice_issued, billing.payment_received | **Complete** | Verified end of August 2026 | **Issued 2026-09-14** | Held temporary 1200/min elevation during parallel run; becomes permanent baseline |
| Fraud Detection | Risk Eng | risk.alert_raised, account.status_changed | **Complete** | Migrated July 2026 | **Issued 2026-09-14** | Earlier PE sign-off noted August 2026; reconfirmed 2026-09-14 |
| Payment Gateway Webhooks | Payments Eng | billing.payment_received, account.status_changed | **Complete** | Completion report 2026-08-28 | **Issued 2026-09-14** | Both subscriptions re-registered, signature validation working, PiSync config removed |
| Analytics Dashboard | Data Eng | account.updated, billing.invoice_issued | **In Progress — at risk** | **Hard internal deadline 2026-11-15** (Priya, 2026-09-14) | Pending | 2 subscriptions scoped (owner: Aisha, recently back from leave). API-key → OAuth2 migration required. IAM block reported resolved (unverified). **Verify actual event volume before finalising scope** — "low volume" label predates new reporting views (James Okafor). Tom Becker notified of deadline |
| Risk Alerts Service | Risk Eng | risk.alert_raised | **In Progress** | General deadline 2026-12-31 | Pending | Completion rumours **unverified** — not Complete under Policy §4. Two open tickets (escalated 2026-08-29): intermittent `X-EventBridge-Signature` validation failures consistent with residual legacy-path traffic. Resolve tickets, submit completion report, obtain PE verification |
| Partner Notification Feed | Partner Eng | partner.event | **Deprecated effective 2026-09-15** (confirmed in writing by PE lead 2026-09-14) | **Sunset 2026-11-30** (accelerated, Policy §2) | — | Reclassified from Maintenance. API-key auth → OAuth2 required. Must complete migration or decommission by 2026-11-30, one month ahead of the general deadline. Partner Eng notified |
| LogArchive Service (+ direct runtime dependents of its storage pipeline) | Infra Eng | account.created, account.updated | **In Progress — formal exception approved 2026-09-14** | Tied to storage backend go-live (Q1 2027 at earliest) | — | Exempt from 2026-12-31 General Sunset Date. Exception explicitly covers direct runtime dependents (supersedes Policy §3 named-service-only default). One-off — not a general extension; no other exceptions exist |
| PiSync compatibility shim (platform) | Platform Eng | — | **Maintenance** (no new registrations) | **Deprecated 2026-10-01; removed 2026-12-31** | — | Removal applies to all services except those under the LogArchive exception |

---

# Part 3 — Consolidated Timeline

| Date | Event |
|---|---|
| **2026-09-15** | Partner Notification Feed becomes **Deprecated** |
| **2026-09-30** | Analytics confirmed completion date due to Priya (per 2026-09-02 thread; the 2026-11-15 hard deadline stands regardless) |
| **2026-10-01** | PiSync compatibility shim enters **Deprecated** |
| **2026-11-01** | **1200 events/min becomes permanent default** delivery rate limit |
| **2026-11-15** | **Analytics Dashboard hard internal migration deadline** |
| **2026-11-30** | **Partner Notification Feed sunset** (Deprecated-service accelerated deadline) |
| **2026-12-31** | **General Sunset Date** — PiSync shim removed; all services without the LogArchive exception must be migrated and PE-verified |
| 2027-01-01 | No rate-limit reversion (superseded) |
| Q1 2027 (earliest) | LogArchive storage backend go-live; LogArchive migration follows |

There is **no "November 1 soft cutoff"** for migration — that rumour was never agreed (Connor Marsh, 2026-07-28); 2026-11-01 is the rate-limit date only.

---

# Part 4 — Immediate Actions for Engineering Leads (today)

1. **Retune all DLQ alerting and retry assumptions to 3 total delivery attempts.** Any logic built on 5 (spec) or 4 (wiki) is wrong against live behaviour.
2. **Validate signatures against `X-EventBridge-Signature` only.** Audit for `X-PiSync-Signature` or `X-EventBridge-Sig` in EventBridge code paths.
3. **Register only via `POST /subscriptions`.** Ticket any staging 404s; do not change the path.
4. **Capacity planning:** keep 1000/min assumptions live until 2026-11-01, then 1200/min permanently; request the elevation now if parallel-running before November.
5. **Analytics, Risk Alerts, Partner Notification Feed owners:** deadlines are 2026-11-15, 2026-12-31, and 2026-11-30 respectively — schedule accordingly; completion requires formal PE verification, not just a done report.
6. **Pull the May draft migration guide from circulation** wherever found; it contains a wrong endpoint and wrong header. Use this document and the v2 spec (with the supersessions noted in §1.4/§1.5).

</deliverable>

---

<assumptions>

## Assumptions, judgment calls, and documentation gaps

1. **Signature header, token endpoint, secret length** — Priya's update is silent; calls made per conflict register #3, #5, #6 (Approved spec + corroborating sources outweigh the error-prone quick reference and the SLA's isolated header error).
2. **Retry backoff schedule under the 3-attempt threshold** is derived from the spec's backoff table (first two intervals) because no document restates the schedule for 3 attempts; the confirmed fact is the threshold itself. Spec update pending (owner: James Okafor).
3. **"3 total attempts" semantics:** the gateway parameter `delivery_retry_max_attempts = 3` could literally read as 3 retries (4 total); Priya's email explicitly resolves this as a naming-convention issue with an effective threshold of **3 total attempts**, on Tariq's confirmation to Lena. That resolution is adopted verbatim as the authoritative position.
4. **Management API rate limit value** (incl. DLQ inspection endpoint) is confirmed to be separate from delivery limits but its number appears in no supplied document — gap.
5. **Completion-date granularity:** CS Tooling ("June 2026") and Fraud Detection ("July 2026") have month-level dates only; Billing Sync is "end of August 2026" (an earlier sync implied late July — the later, verification-bearing record was used). Payment Gateway Webhooks has the only day-precise marker (report 2026-08-28). Formal PE sign-off for all four: 2026-09-14.
6. **Staging 404s on `POST /subscriptions`** remain unresolved as of the Slack export (2026-09-12); treated as an environment defect per James's determination, not a path change.
7. **Analytics IAM resolution and event volume** are unverified in the supplied materials; the 2026-11-15 deadline and the volume-verification instruction stand regardless.
8. **LogArchive exception scope** beyond "direct runtime dependency on the LogArchive storage pipeline" is not enumerated; the Sep 10 sync's written scope document (James's action) is referenced but not among the supplied files — dependent teams should confirm coverage with Platform Engineering before relying on the exemption. Priya's formal approval (2026-09-14) is taken as satisfying the approval condition she set on 2026-09-10.
9. **Referenced but unavailable artifacts:** the OAuth2 onboarding wiki page, the internal wiki page citing "4 failures", the LogArchive exception scope document, the "internal migration guide" cited by the Vantix partner team (plausibly the May draft — unconfirmed), and the pre-Sep-14 "email from Priya confirming 3" cited in two support tickets (never located; now moot given the 2026-09-14 confirmation). Noted and proceeded without them.
10. **Pending documentation updates** (announced, not yet published as of 2026-09-14): spec v2 DLQ section and rate-limit section; v2.1 release notes rate-limit characterisation; quick reference corrections; tracker refresh. Until published, this document reflects the confirmed positions.

</assumptions>
