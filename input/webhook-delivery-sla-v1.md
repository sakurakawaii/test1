# EventBridge Webhook Delivery SLA — v1.0

**Status:** Approved  
**Owner:** Platform Engineering  
**Last Updated:** 2026-06-15  
**Applies to:** All internal services consuming EventBridge webhook delivery  
**Review cycle:** Annually or on major platform release

---

## Purpose

This document defines the delivery service level commitments for the EventBridge platform, the compliance requirements for receiving endpoints, and the operational guarantees teams can rely on when building integrations.

---

## Delivery Commitments

| Metric | Commitment |
|---|---|
| Delivery latency (p50) | < 2 seconds from event emission to first delivery attempt |
| Delivery latency (p99) | < 15 seconds from event emission to first delivery attempt |
| Retry attempts before DLQ | 3 consecutive failures |
| DLQ event retention | 14 days |
| Platform availability | 99.9% monthly uptime (excluding scheduled maintenance) |
| Scheduled maintenance notice | Minimum 48 hours via #platform-eng |

### Retry policy detail

EventBridge retries delivery on any non-2xx response or endpoint timeout. After **3 consecutive delivery failures**, the event is considered undeliverable for automatic retry and moved to the subscription's Dead Letter Queue. Teams should design consumer alerting around this threshold.

The retry schedule uses fixed exponential delays. Events that reach the DLQ are available for manual replay via the management API; automated replay is not currently supported.

---

## Receiving Endpoint Requirements

To be compliant with EventBridge delivery, a receiving endpoint must:

1. **Accept HTTPS only.** HTTP endpoints will be rejected at subscription creation. Your endpoint must present a valid TLS certificate.

2. **Return 2xx within 10 seconds.** Any other response code or a timeout counts as a delivery failure toward the DLQ threshold.

3. **Validate the delivery signature.** Every EventBridge delivery request includes a signature computed as HMAC-SHA256 of the raw request body using the subscription secret. Receiving endpoints must validate this signature to ensure delivery integrity.

   The signature is transmitted in the delivery header. Validate using your subscription secret:

   ```python
   import hmac, hashlib

   def validate_delivery(body_bytes, secret, header_value):
       expected = "sha256=" + hmac.new(
           secret.encode(), body_bytes, hashlib.sha256
       ).hexdigest()
       return hmac.compare_digest(expected, header_value)
   ```

   The header carrying this signature is `X-PiSync-Signature`. Endpoints that do not validate this header are out of compliance with EventBridge delivery requirements.

4. **Be idempotent.** EventBridge guarantees at-least-once delivery. Under retry conditions, your endpoint may receive the same `event_id` more than once. Consumer logic must handle duplicate delivery.

5. **Not return 5xx for business-logic reasons.** A 5xx tells EventBridge that delivery failed and triggers retry. If your endpoint successfully processed an event but encountered a downstream error, return 2xx and handle the downstream error independently.

---

## Rate Limits

Default delivery rate: **1000 events/min per subscription**. This is the platform-standard limit.

Elevated limits are available on request for services with documented high-volume requirements. Contact #platform-eng with your `service_id` and expected event volume.

---

## Subscription Limits

- Maximum active subscriptions per service: 200
- Maximum secret length: 256 characters (minimum: 32 characters)
- Topic wildcards: family-level wildcards (e.g. `account.*`) only; global `*` is not supported

---

## Incident and Escalation

For delivery failures or platform issues:
- Real-time status: #platform-eng
- Escalation path for production incidents: Platform Engineering on-call (via PagerDuty)
- DLQ events older than 13 days should be escalated — they expire in 14 days with no automated replay

---

## Changelog

- **v1.0** (2026-06-15): Initial publication covering EventBridge v2.0 delivery guarantees.

---

*This document is reviewed annually. For questions, contact #platform-eng.*

