# EventBridge Migration Reference — Consolidated Engineering Guidance

**Document date:** 2026-09-14
**Primary authority:** Priya Nair consolidated status email, 2026-09-14 ("treat this as the current authoritative position from Platform Engineering")
**Supporting sources:** EventBridge API Spec v2.0.1 (Approved), Webhook Delivery SLA v1.0 (Approved), Release Notes v2.1.0 (Final), Migration Policy v2.0 (Approved, effective 2026-09-01), migration status tracker, engineering sync notes (08-05 / 08-18 / 09-10), email threads (DLQ policy, DLQ escalation, rate limit, Analytics), #platform-eng Slack export (2026-09-12), support ticket summary (to 2026-09-08), Technical Quick Reference v1, archived PiSync v1 spec, draft migration guide (unpublished)
**Intended audience:** Engineering leads and integration teams completing the PiSync → EventBridge migration

---

<summary>

This document consolidates all supplied artifacts into a single actionable reference for the final migration sprint. The Priya Nair email of 2026-09-14 closes the three major open disputes and is used as the controlling authority:

1. **DLQ threshold is 3 total delivery attempts** — the v2.0.1 spec value of 5 was a documentation error. Confirmed against the live gateway configuration (`delivery_retry_max_attempts = 3`, extracted by Platform Operations 2026-09-12) and confirmed in writing by the infrastructure lead.
2. **Rate limit: 1200 events/min becomes the permanent default on 2026-11-01** — VP sign-off received 2026-09-12. This supersedes the v2.1 release notes' "temporary elevation" framing. Until 2026-10-31 the default remains 1000/min with 1200/min available on request.
3. **Service statuses resolved:** four services are Complete with Platform Engineering sign-off issued 2026-09-14 (CS Tooling, Billing Sync, Fraud Detection, Payment Gateway Webhooks); Partner Notification Feed is **Deprecated effective 2026-09-15 with an accelerated sunset of 2026-11-30**; Analytics Dashboard has a **hard internal deadline of 2026-11-15**; LogArchive (plus directly dependent logging services) holds a **formally approved exception** to the 2026-12-31 sunset.

Where Priya's update is silent (signature header name, registration endpoint path, OAuth token endpoint, secret length, retry delay intervals), this document makes a definitive call based on the strongest available evidence, documented in the analysis section. Known documentation errors in otherwise Approved documents (SLA v1.0 signature header; Technical Quick Reference token endpoint, secret length, and retry schedule) are identified so teams do not act on them.

</summary>

---

<analysis>

## Conflict Register and Resolutions

Each conflict below was resolved either by the 2026-09-14 Priya Nair email (authoritative) or, where that email is silent, by the strongest corroborated evidence. Newest-document status was not assumed to be correct — several recently updated or Approved documents contain verified errors.

| # | Topic | Conflicting claims | Resolution | Basis |
|---|---|---|---|---|
| 1 | DLQ threshold | Spec v2.0.1: **5** (calls 3 the error) · Release notes v2.1 + SLA v1.0: **3** · Slack/wiki rumors: 4 · Sep 10 sync working assumption: 5 | **3 total delivery attempts** | Priya 2026-09-14 (controlling). Corroborated by live gateway config extract `delivery_retry_max_attempts = 3` (Nadia Osei, Platform Ops, 2026-09-12) and Tariq Bashir's confirmation to Lena Vasquez. The spec's "5" was a drafting error. |
| 2 | Retries vs. total attempts | Nadia's reading of the config parameter implied possibly 4 total (initial + 3 retries); Tariq initially could not resolve it | **3 total attempts** — the parameter name is a naming-convention artifact, not a behavioural difference | Priya 2026-09-14, citing Tariq's confirmation: "the effective threshold is 3 total delivery attempts" |
| 3 | Rate limit permanence | v2.1 notes + SLA + spec: 1200 temporary, reverts to 1000 on 2027-01-01 · James 2026-09-03 email: permanent from Nov 1 (retracted as premature at Sep 10 sync — VP sign-off outstanding) | **1200/min permanent default from 2026-11-01** | Priya 2026-09-14: VP sign-off received 2026-09-12. James's Sep 3 email supplies the operational mechanics (automatic application, delivery-only), now validated. |
| 4 | Delivery signature header | Spec v2.0.1 + Quick Ref + archived PiSync mapping: `X-EventBridge-Signature` · SLA v1.0 §3: `X-PiSync-Signature` required for compliance · Draft guide: `X-PiSync-Signature` · One unidentified doc: `X-EventBridge-Sig` | **`X-EventBridge-Signature`** | Priya silent — call made. Spec (Approved, current) is explicit; support empirically resolved 8 tickets by confirming EventBridge deliveries carry `X-EventBridge-Signature` and that `X-PiSync-Signature` is absent. The SLA v1.0 compliance sentence is an error (published 2026-06-15, pre-dating the spec clarification). |
| 5 | Registration endpoint | Spec: `POST /subscriptions` · Draft guide: `POST /webhooks/register` (author's own TODO flags uncertainty) · Slack rumor: `/v2/subscriptions` | **`POST /subscriptions`** | Priya silent — call made. Spec is explicit; James Okafor confirmed in #platform-eng (2026-09-08) the documented path stands and staging 404s are an environment issue, not a path change. `/webhooks/register` is the legacy PiSync endpoint and rejects new registrations. |
| 6 | OAuth token endpoint | Spec + draft guide: `https://auth.pitaron.io/oauth/token` · Quick Ref: `https://auth.pitaron.internal/v1/oauth/token` | **`https://auth.pitaron.io/oauth/token`** | Priya silent — call made. Two independent sources agree with the spec; the Quick Ref contains multiple other verified errors (see #7, #8) and is treated as unreliable on contested values despite its Approved status. |
| 7 | Minimum secret length | Spec: 32 · SLA: 32 (max 256) · Quick Ref: 16 | **Minimum 32, maximum 256 characters** | Spec and SLA agree; Quick Ref value is an error. |
| 8 | Retry schedule | Spec: exponential backoff · Quick Ref table: "fixed 60 seconds" (its own footnote admits the table shows legacy PiSync values) | **Exponential backoff** (see derived schedule in deliverable) | Spec; the fixed 60-second interval is PiSync legacy behaviour only. |
| 9 | Rate limit "current default" | Quick Ref (2026-08-20) lists 1200 as the default and 1000 as "legacy pre-November 1" | Incorrect at time of publication; the default remains **1000/min until 2026-10-31**, then 1200/min | Spec + SLA for current state; Priya 2026-09-14 for the Nov 1 change. |
| 10 | Payment Gateway Webhooks status | Tracker (2026-07-01): In Progress · Completion report submitted 2026-08-28; no PE sign-off as of Sep 10 sync (Pending Confirmation under Policy §4) | **Complete** | Priya 2026-09-14 issued formal Platform Engineering sign-off, satisfying Policy v2.0 §4/§6. |
| 11 | Partner Notification Feed status | Tracker: Maintenance · Data-team email claimed Deprecated (unconfirmed at Sep 10 sync) | **Deprecated effective 2026-09-15; sunset 2026-11-30** | Priya 2026-09-14 — constitutes the written Platform Engineering confirmation that Policy v2.0 §2 requires to trigger the accelerated deadline. |
| 12 | LogArchive exception scope | Policy v2.0 §3: exceptions cover only the named service; dependents must apply separately · Sep 10 sync: approval conditional on written scope by Sep 30 | **Exception formally approved for LogArchive and services with a direct runtime dependency on the LogArchive storage pipeline** | Priya 2026-09-14: "I've approved this formally." This is a documented, approved exception that deliberately extends beyond the policy's named-service rule; preserved as decided. |
| 13 | "November 1 soft cutoff" for migration | Referenced in 3 support tickets and earlier emails | **No such migration deadline exists.** 2026-11-01 is the rate-limit permanence date only | Connor Marsh 2026-07-28 ("No such date has been agreed"); support ticket summary; Priya's email assigns no migration meaning to Nov 1. |
| 14 | Risk Alerts Service completion | James "heard it was done" (Sep 10 sync); Marcus Webb (owning team) could not confirm; webhook validation possibly still open | **Not complete — In Progress** | Risk Alerts is absent from Priya's confirmed-complete list; two open support tickets show intermittent signature failures consistent with partial legacy-path traffic. No completion report or sign-off exists (Policy §6 unmet). |
| 15 | Billing Sync completion date | Aug 5 sync: "done as of last week" · Sep 10 sync: "migrated and verified end of August" | **Verified end of August 2026** | The verified date from the most recent sync is used; PE sign-off 2026-09-14. |

**Documents that must not be used as technical guidance:** the draft migration guide (Connor Marsh, May 2026 — unpublished, flagged superseded at the 2026-08-05 sync, contains the wrong endpoint and wrong header); the archived PiSync v1 spec (historical reference and field-mapping only); the Technical Quick Reference v1 on any value contested above; the SLA v1.0 §3 header sentence; and the spec v2.0.1 DLQ/rate-limit sections pending James Okafor's announced documentation update.

</analysis>

---

<deliverable>

# Part 1 — Definitive Technical Configuration Values

Engineers should implement against the values below, effective immediately.

## 1.1 Authentication (management API)

| Parameter | Value |
|---|---|
| Method | OAuth2 client credentials (API keys **not** supported by EventBridge) |
| Token endpoint | `POST https://auth.pitaron.io/oauth/token` |
| Grant type | `client_credentials` |
| Scopes | `eventbridge:read eventbridge:write` (write required for create/delete; read for list/inspect) |
| Token lifetime | 3600 seconds — refresh with at least a 5-minute buffer |
| Recommended client | `pitaron-auth-client` v2.4+ (automatic refresh); non-JVM runtimes: OAuth2 onboarding guide, Platform Eng wiki |
| Credential provisioning | IAM portal |

```
POST https://auth.pitaron.io/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=eventbridge:read eventbridge:write
```

## 1.2 Subscription management

| Operation | Method and path |
|---|---|
| Create subscription | `POST /subscriptions` |
| List subscriptions | `GET /subscriptions?service_id={id}` (optional filters: `topic`, `status` = active/paused/errored) |
| Get subscription | `GET /subscriptions/{subscription_id}` |
| Delete subscription | `DELETE /subscriptions/{subscription_id}` (in-flight deliveries complete; no new dispatch) |
| Inspect DLQ | `GET /subscriptions/{subscription_id}/dlq` (paginated via `cursor`) |

**Create request body** (field names changed from PiSync — see §1.7):

```json
{
  "service_id": "your-service-id",
  "topic": "account.updated",
  "endpoint_url": "https://your-service.pitaron.internal/webhooks/incoming",
  "secret": "hmac-secret-32-to-256-characters"
}
```

| Constraint | Value |
|---|---|
| Max active subscriptions per service | 200 (exceeding returns `400 subscription_limit_exceeded`) |
| Secret length | Minimum 32, maximum 256 characters |
| Endpoint protocol | HTTPS only, valid TLS certificate; must be reachable from the EventBridge delivery network |
| Duplicate registration | `409 duplicate_subscription` for same service_id + topic + endpoint_url |

**Do not use:** `POST /webhooks/register` (legacy PiSync — rejects new registrations) or `/v2/subscriptions` (unverified rumor, rejected by Platform Engineering). **Known issue:** `POST /subscriptions` returning 404 **in staging** is an unresolved staging-environment problem reported by three teams (escalated 2026-09-08) — open a ticket; do not change the path.

## 1.3 Delivery contract (receiving endpoints)

| Parameter | Value |
|---|---|
| Delivery method | HTTP POST to registered `endpoint_url` |
| Required response | 2xx within **10 seconds**; anything else (including timeout) counts as a delivery failure |
| Signature header | **`X-EventBridge-Signature`** — value format `sha256=<hex>` |
| Signature algorithm | HMAC-SHA256 of the raw request body using the subscription `secret` |
| Delivery semantics | At-least-once; consumers **must be idempotent** on `event_id` |
| 5xx usage | Never return 5xx for business-logic failures — it triggers retry; return 2xx and handle downstream errors independently |

Do **not** validate `X-PiSync-Signature` (absent on EventBridge deliveries; legacy shim traffic only) and do not use `X-EventBridge-Sig` (an error from an unidentified internal document). The SLA v1.0 sentence naming `X-PiSync-Signature` as the compliance header is a known documentation error.

```python
import hmac, hashlib

def validate(body_bytes, secret, header_value):  # header_value = X-EventBridge-Signature
    expected = "sha256=" + hmac.new(secret.encode(), body_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header_value)
```

**Event shape:** `event_id` (prefix `evt_`), `topic`, `payload`, `timestamp` (ISO-8601 UTC), `version: "2"`.

## 1.4 Retry and Dead Letter Queue — CONFIRMED 2026-09-14

| Parameter | Value |
|---|---|
| **DLQ threshold** | **3 total delivery attempts** (initial attempt + 2 retries), then the event moves to the DLQ |
| Live gateway parameter | `delivery_retry_max_attempts = 3` (Platform Ops config extract, 2026-09-12; parameter name is a naming convention — effective behaviour is 3 total attempts per Platform Engineering) |
| Retry trigger | Any non-2xx response or timeout |
| Backoff | Exponential. Derived effective schedule: initial attempt → retry after 30 s → retry after 2 min → DLQ. (Delays taken from the spec's backoff table; the 10-min and 30-min steps listed there never execute under the confirmed 3-attempt threshold.) |
| DLQ retention | 14 days, then events expire permanently |
| Replay | Manual only via `GET /subscriptions/{subscription_id}/dlq`; automated replay not available |
| Operational rule | Escalate DLQ events older than 13 days — no automated recovery after expiry |

**Action required:** tune consumer alerting and retry-dependent logic to **3**. The v2.0.1 spec's "5 consecutive failed delivery attempts" (and its note calling 3 the error) is a confirmed documentation error; the spec is being corrected. Any team that built for 5 should review immediately — events reach the DLQ two attempts earlier than that assumption. The earlier "use 5 as a working assumption" guidance (Slack, Aug 12/29; sync decisions Aug 18 and Sep 10) is **rescinded** by the 2026-09-14 confirmation.

## 1.5 Rate limits — CONFIRMED 2026-09-14

| Period | Default delivery limit | Notes |
|---|---|---|
| Now → 2026-10-31 | 1000 events/min per subscription | 1200/min elevation available on request in #platform-eng for parallel-run services |
| **From 2026-11-01** | **1200 events/min per subscription — permanent** | VP of Infrastructure sign-off received 2026-09-12; applies automatically to all services; no request needed; no reversion on 2027-01-01 |

- Teams that designed for 1000/min as the permanent floor should revise capacity planning; teams may design for 1200/min as the permanent baseline for post-Nov-1 operation.
- Services already holding the parallel-run elevation keep 1200/min with no action; it simply becomes their permanent baseline.
- The 1200/min figure applies to **event delivery only**. The management API (including DLQ inspection) has a separate limit, unaffected by this change (value not documented in supplied materials — see assumptions).
- Rate limit headers on management API responses: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- Migration Policy v2.0 §5 (elevation expiry 2026-12-31, no extension for exception services) is rendered moot from 2026-11-01: exception-holding services (LogArchive group) receive the permanent 1200/min default like everyone else.

## 1.6 Delivery SLA commitments (unchanged, SLA v1.0)

| Metric | Commitment |
|---|---|
| Delivery latency p50 / p99 | < 2 s / < 15 s from emission to first delivery attempt |
| Platform availability | 99.9% monthly uptime (excluding scheduled maintenance) |
| Scheduled maintenance notice | ≥ 48 hours via #platform-eng |

## 1.7 Topics and PiSync field mapping

Topics: `account.created`, `account.updated`, `account.status_changed`, `billing.invoice_issued`, `billing.payment_received`, `risk.alert_raised`, `partner.event`. Wildcards: family-level only (`account.*`); global `*` not supported. Known cosmetic issue: wildcard subscriptions are not filtered by sub-type in `GET /subscriptions` listings; delivery behaviour is correct.

| PiSync (legacy) | EventBridge |
|---|---|
| `POST /webhooks/register` + `X-Api-Key` | `POST /subscriptions` + OAuth2 bearer token |
| `service_name` / `event_type` / `target_url` / `signing_secret` | `service_id` / `topic` / `endpoint_url` / `secret` |
| `webhook_id` | `subscription_id` |
| `X-PiSync-Signature` | `X-EventBridge-Signature` |
| 3 retries, fixed 60 s interval | 3 total attempts, exponential backoff (§1.4) |
| 500 events/min default | 1000/min now; 1200/min permanent from 2026-11-01 |

Migration completion checklist (Policy v2.0 §6 — all four required): (1) all PiSync subscriptions deregistered or confirmed inactive; (2) EventBridge subscriptions active and delivering; (3) completion report submitted to Platform Engineering; (4) formal written Platform Engineering verification issued. Support-ticket closure does not count as verification. Remove `PISYNC_API_KEY` from service config at cutover.

---

# Part 2 — Per-Service Migration Status

Status as of 2026-09-14, incorporating Platform Engineering sign-offs issued in Priya Nair's email of that date.

| Service | Owner team | Topics | Status | Completion / deadline date | Notes |
|---|---|---|---|---|---|
| CS Tooling | Customer Success Eng | account.updated, account.status_changed | **Complete — PE sign-off issued** | Migrated June 2026; sign-off 2026-09-14 | No issues reported |
| Billing Sync | Finance Eng | billing.invoice_issued, billing.payment_received | **Complete — PE sign-off issued** | Migrated and verified end of August 2026; sign-off 2026-09-14 | Held parallel-run elevation; 1200/min becomes permanent baseline 2026-11-01 |
| Fraud Detection | Risk Eng | risk.alert_raised, account.status_changed | **Complete — PE sign-off issued** | Migrated July 2026; sign-off 2026-09-14 | — |
| Payment Gateway Webhooks | Payments Eng | billing.payment_received, account.status_changed | **Complete — PE sign-off issued** | Completion report 2026-08-28; sign-off 2026-09-14 | Both subscriptions re-registered, signature validation verified, PiSync config removed; tracker (last updated 2026-07-01) is stale and must be updated |
| Analytics Dashboard | Data Eng | account.updated, billing.invoice_issued | **In Progress — at risk; hard deadline set** | **Must complete by 2026-11-15** (internal deadline, earlier than general sunset) | Two subscriptions scoped (owner: Aisha, returning from leave ~2026-09-15). Requires API-key → OAuth2 auth migration; IAM provisioning reported resolved (unverified). Event volume must be re-verified before finalising scope — "low volume" classification predates new reporting views. Tom Becker notified. |
| Risk Alerts Service | Risk Eng | risk.alert_raised | **In Progress — not verified** | General deadline 2026-12-31; Q4 target | Not on the confirmed-complete list. Two open support tickets: intermittent signature-validation failures consistent with residual legacy-path traffic. Owning team could not confirm completion at the 2026-09-10 sync. Must confirm remaining PiSync traffic is eliminated and submit a completion report per Policy §6. |
| Partner Notification Feed | Partner Eng | partner.event | **Deprecated effective 2026-09-15** | **Sunset 2026-11-30** (accelerated per Policy v2.0 §2) | Reclassified from Maintenance with written PE confirmation (Priya, 2026-09-14) — the accelerated deadline is therefore in force. API-key auth; full OAuth2 + re-registration required. Partner Eng notified separately. |
| LogArchive Service (+ direct runtime dependents on the LogArchive storage pipeline) | Infra Eng | account.created, account.updated | **In Progress — approved exception** | Exempt from 2026-12-31; tied to storage backend go-live (Q1 2027 at earliest) | Exception formally approved 2026-09-14; scope explicitly includes directly dependent logging services (an approved departure from Policy §3's named-service rule). One-off — not a general extension. No separate rate-limit arrangement needed post-2026-11-01 (permanent 1200/min default applies). |

**PiSync compatibility shim:** Maintenance now → **Deprecated 2026-10-01** → **Removed 2026-12-31** (General Sunset Date). New registrations via the legacy endpoint are already rejected.

---

# Part 3 — Confirmed Decisions Log

| Decision | Value | Decided / confirmed | Authority |
|---|---|---|---|
| DLQ threshold | 3 total delivery attempts | 2026-09-14 (config extract 2026-09-12) | Priya Nair, with gateway/infrastructure written confirmation |
| Rate limit permanence | 1200 events/min permanent default from 2026-11-01 | VP sign-off 2026-09-12; announced 2026-09-14 | VP of Infrastructure; Priya Nair |
| Partner Notification Feed reclassification | Deprecated effective 2026-09-15; sunset 2026-11-30 | 2026-09-14 | Priya Nair (written PE confirmation per Policy §2) |
| Analytics Dashboard deadline | Hard internal deadline 2026-11-15 | 2026-09-14 | Priya Nair |
| LogArchive exception | LogArchive + direct runtime dependents exempt from 2026-12-31, tied to storage backend go-live | Agreed 2026-09-10 sync; formally approved 2026-09-14 | Priya Nair |
| Completion sign-offs | CS Tooling, Billing Sync, Fraud Detection, Payment Gateway Webhooks | 2026-09-14 | Platform Engineering |
| PiSync shim timeline | Deprecated 2026-10-01; removed 2026-12-31 | Spec v2.0.1 / Release notes v2.1 / Policy v2.0 | Platform Engineering |
| "November 1 soft cutoff" | Does not exist as a migration deadline | 2026-07-28, reaffirmed by omission 2026-09-14 | Connor Marsh / Platform Engineering |

## Key dates at a glance

| Date | Event |
|---|---|
| 2026-09-15 | Partner Notification Feed becomes Deprecated |
| 2026-09-30 | LogArchive exception scope documentation deadline from the 2026-09-10 sync (exception subsequently approved 2026-09-14; treat scope paperwork as an administrative follow-up, not a gating condition) |
| 2026-10-01 | PiSync compatibility shim enters Deprecated |
| 2026-11-01 | 1200 events/min becomes the permanent default delivery rate limit |
| 2026-11-15 | Analytics Dashboard hard migration deadline |
| 2026-11-30 | Partner Notification Feed sunset (Deprecated-status accelerated deadline) |
| 2026-12-31 | General Sunset Date — PiSync shim removed for all services without an approved exception |
| Q1 2027 (earliest) | LogArchive storage backend go-live; LogArchive group migration follows |

## Guidance superseded or invalidated — do not act on

- Draft migration guide (May 2026): wrong endpoint (`/webhooks/register`), wrong header (`X-PiSync-Signature`); never published, flagged superseded.
- Spec v2.0.1 DLQ section ("5 attempts", "correct threshold has always been 5") and rate-limit section (1200 reverts 2027-01-01): documentation error / superseded; correction in progress (James Okafor).
- SLA v1.0 §3 compliance sentence naming `X-PiSync-Signature`: documentation error. (The SLA's DLQ threshold of 3 and all other values remain valid.)
- Technical Quick Reference v1: token endpoint, 16-character minimum secret, "fixed 60 s" retry row, and rate-limit table labelling are all incorrect; use this document instead.
- "Use 5 as the working assumption" (Slack 2026-08-12/29; sync decisions 2026-08-18 and 2026-09-10): rescinded.
- James Okafor's 2026-09-03 rate-limit email: framing was premature at the time but its content is now confirmed; rely on the 2026-09-14 announcement.
- Connor Marsh's "no exceptions to December 31" position: superseded by the approved LogArchive exception.

</deliverable>

---

<assumptions>

## Assumptions, Judgment Calls, and Gaps

1. **Management API base URL.** No current document states the full host for the management API; only paths are documented. The only host evidence is `https://eventbridge.pitaron.internal` in the unpublished draft guide (attached to the wrong path). Paths in Part 1 are therefore given relative; teams should confirm the host via #platform-eng before first use. *Gap.*
2. **Retry delay intervals (30 s, 2 min).** The confirmed facts are: threshold = 3 total attempts, backoff = exponential. The specific delays are derived by truncating the v2.0.1 spec's backoff table at the confirmed threshold. No post-correction document restates the delays. Marked as derived in §1.4. *Judgment call.*
3. **Management API rate limit value.** Confirmed to exist and to be separate from the delivery limit (James Okafor, 2026-09-03 thread) but no figure appears in any supplied material. *Gap.*
4. **Staging 404 on `POST /subscriptions`.** Unresolved as of the latest artifacts (three teams affected, escalated 2026-09-08). Treated as an environment defect per Platform Engineering's position, not a path change. *Open operational issue, not a documentation conflict.*
5. **LogArchive exception paperwork.** The 2026-09-10 sync conditioned approval on written dependency confirmation and a scope document by 2026-09-30; Priya's 2026-09-14 email states the exception is formally approved and defines scope. The later, authoritative statement is treated as controlling, with the written scope document assumed to be an administrative follow-up. The precise list of "directly dependent" logging services is not enumerated in any supplied artifact. *Judgment call + gap.*
6. **Analytics event volume.** James Okafor's concern that Analytics volume exceeds its "low volume" classification is flagged but unverified in the supplied materials; Priya's 2026-11-15 deadline partially prices in this risk. Volume verification is listed as a required action, not a confirmed fact. *Gap.*
7. **Risk Alerts Service.** Classified In Progress by inference: it is absent from Priya's confirmed-complete list, the owning team could not confirm completion, no completion report exists, and open tickets indicate residual legacy-path traffic. No artifact states its status explicitly post-2026-09-10. *Judgment call.*
8. **DLQ attempt counting.** Priya's "3 total delivery attempts" is adopted as final. Note that Platform Operations' raw reading of `delivery_retry_max_attempts = 3` could imply 4 total attempts (initial + 3 retries); Priya explicitly characterises this as a parameter-naming convention with an effective threshold of 3 total. Teams observing behaviour inconsistent with 3 total attempts should raise it in #platform-eng with evidence. *Resolved by authority; residual ambiguity noted for operational vigilance.*
9. **Referenced but unavailable materials.** The OAuth2 onboarding guide (Platform Eng wiki), the IAM portal documentation, the June 3 maintenance-window change log, the internal wiki page citing "4 failures", the document instructing `X-EventBridge-Sig`, and the "internal migration guide" cited by the Vantix partner team were not supplied; conclusions do not depend on them. *Noted absences.*
10. **Tracker staleness.** The migration status tracker (last updated 2026-07-01) is outdated for Billing Sync, Payment Gateway Webhooks, Analytics (IAM note), and Partner Notification Feed. Part 2 of this document supersedes it pending Sofia Andrade's update. *Documented.*

</assumptions>
