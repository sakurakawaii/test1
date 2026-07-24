# Release Notes — EventBridge v2.1.0

**Published:** 2026-07-15  
**Status:** Final  
**Audience:** All engineering teams integrating with EventBridge

---

## Summary

v2.1.0 is a minor release addressing documentation accuracy, retry policy clarification, and a temporary rate limit elevation to support parallel-run operations during the PiSync migration window. There are no breaking changes to existing v2 consumers.

---

## Enhancements

### Dead Letter Queue threshold — documentation correction

The v2.0 launch specification incorrectly documented the DLQ threshold as **5 consecutive delivery failures**. This was a documentation error introduced during the initial drafting cycle that did not reflect the deployed gateway configuration. The correct threshold is **3 consecutive failures**, after which the event is moved to the subscription's Dead Letter Queue.

Teams that planned retry handling or alerting thresholds based on the incorrect figure of 5 should review their configuration. Any integration that has been observing events reaching the DLQ after a third delivery failure was already aligned with actual behavior.

### Signature header name clarification

Several teams have asked about the difference between `X-PiSync-Signature` (present on legacy PiSync deliveries) and EventBridge's delivery signature header. To be explicit:

- EventBridge deliveries carry a delivery signature for validation. Confirm the exact header name in the current v2 spec — this was one of the items still being finalized as these notes were prepared.
- `X-PiSync-Signature` — present on legacy PiSync deliveries coming through the compatibility shim. Do not use this header for EventBridge integrations.

### Migration window rate limit elevation

To support services running EventBridge and PiSync in parallel during the cutover period, an elevated delivery rate limit of **1200 events/min per subscription** is available on request through 2026-12-31. This elevation is available from the date of this release.

**This limit is temporary.** The standard limit of 1000 events/min will be restored on 2027-01-01 unless superseded by a subsequent announcement. Teams should not design for 1200 events/min as a permanent capacity floor without confirmation.

To request the elevation for your service, open a request in #platform-eng with your `service_id` and the duration you expect to need the parallel run.

---

## Bug Fixes

- Fixed an edge case where `DELETE /subscriptions/{subscription_id}` could return `204` before all in-flight events had acknowledged, leading to some events failing delivery silently after the subscription was removed.
- Corrected an issue where `GET /subscriptions/{subscription_id}/dlq` would return a `500` if the DLQ contained more than 500 events. Pagination is now enforced with a `cursor` parameter.

---

## Known Issues

- Topic wildcard subscriptions (e.g. `account.*`) do not currently filter by topic sub-type when listed via `GET /subscriptions`. All matching subscriptions are returned regardless of wildcard scope. This is cosmetic — delivery behavior is correct.
- Subscription status can show `errored` briefly after a transient network partition even if delivery later succeeds. The status self-corrects on the next successful delivery.

---

## Documentation

- Full endpoint reference: `eventbridge-api-spec-v2.md`
- OAuth2 onboarding for EventBridge: Platform Engineering wiki (link from #platform-eng)

---

## Migration Timeline Reminder

The PiSync compatibility shim enters **Deprecated** status on **2026-10-01**. Planned removal is **2026-12-31**. Teams still on PiSync should have migration work scheduled before this date.

