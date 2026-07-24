# EventBridge Migration Policy — v2.0

**Status:** Approved  
**Owner:** Platform Engineering  
**Approved by:** Priya Nair, Platform Engineering Lead  
**Effective date:** 2026-09-01  
**Supersedes:** EventBridge Migration Policy v1.0 (2026-04-15)

---

## 1. General Sunset Date

All internal services using PiSync must complete migration to EventBridge no later than
**2026-12-31** (the "General Sunset Date"). The PiSync compatibility shim will be removed
on this date for all services not covered by an approved exception (§3).

---

## 2. Integration Status Definitions and Deadlines

Integration statuses have the following migration implications:

| Status | Definition | Sunset Deadline |
|---|---|---|
| Active | Full support, new integrations permitted | N/A — EventBridge only |
| Maintenance | Existing integrations continue; no new PiSync integrations | 2026-12-31 |
| Deprecated | Temporary support only; removal is planned | **2026-11-30** |
| Sunset | Removal is imminent | Already past deadline |
| Removed | No longer supported | N/A |

Services reclassified from Maintenance to Deprecated are subject to the Deprecated sunset
date of **2026-11-30**, regardless of when reclassification occurs. A service reclassified
to Deprecated after 2026-11-01 has fewer than 30 days to complete migration.

Reclassification to Deprecated requires written confirmation from the Platform Engineering
lead. Informal status changes (e.g., communicated via email or Slack without formal
documentation) do not trigger the accelerated deadline until confirmed in writing by
Platform Engineering.

---

## 3. Infrastructure Dependency Exceptions

A service may apply for an exception to the General Sunset Date if migration is blocked
by an infrastructure dependency outside the service team's control.

**Eligibility criteria:**
- a. Written request from the requesting service team's VP or Director
- b. Written confirmation of the dependency and expected resolution date from the
  relevant infrastructure team lead
- c. Formal written approval from the Platform Engineering lead

A service that has met conditions (a) and (b) but is awaiting condition (c) is **not
yet excepted** and remains subject to the General Sunset Date.

Exceptions cover only the specific service named in the approval. Related or dependent
services must apply separately.

**Scope of exception:** The exception suspends the General Sunset Date for the named
service only. It does not extend the temporary rate limit elevation (§5), which expires
on the General Sunset Date regardless of exception status.

---

## 4. Pending Confirmation Services

A service for which a completion report has been submitted to Platform Engineering but
for which formal verification has not been issued is classified as **Pending
Confirmation**. Such services:

- Remain subject to the General Sunset Date
- Must receive formal Platform Engineering verification before 2026-12-31
- Are not treated as "Complete" for planning or reporting purposes until verification
  is issued

A support team ticket closure does not constitute Platform Engineering verification.

---

## 5. Temporary Rate Limit Elevation

The temporary delivery rate limit elevation to 1200 events/min, available on request
during the migration window, expires **2026-12-31**. This expiry is not extended for
services with approved Infrastructure Dependency Exceptions. Services whose migration
extends past the General Sunset Date under an exception must request a separate
arrangement for continued elevated limits from Platform Engineering.

---

## 6. Migration Completion Reporting

Migration is complete only when:
1. All PiSync subscriptions for the service have been deregistered or are confirmed
   inactive (via shim removal or explicit deregistration where available)
2. All EventBridge subscriptions are active and delivering events
3. A completion report has been submitted to Platform Engineering
4. Platform Engineering has issued formal written verification

---

## Changelog

- **v2.0** (2026-09-01): Introduced Deprecated accelerated deadline (2026-11-30).
  Clarified exception scope (named service only). Added Pending Confirmation
  classification. Aligned with current integration status definitions.
- **v1.0** (2026-04-15): Initial policy.

