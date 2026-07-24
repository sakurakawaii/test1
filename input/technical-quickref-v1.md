# EventBridge Technical Quick Reference

**Status:** Approved  
**Owner:** Platform Engineering — Developer Experience  
**Reviewed by:** Connor Marsh, Lena Vasquez  
**Last updated:** 2026-08-20  
**Audience:** Engineering teams implementing EventBridge integrations

---

This quick reference consolidates the most commonly needed values for EventBridge
integrations. For full endpoint documentation see the EventBridge API spec.

---

## Authentication

| Parameter | Value |
|---|---|
| Token endpoint | `https://auth.pitaron.internal/v1/oauth/token` |
| Grant type | `client_credentials` |
| Required scopes | `eventbridge:write` |
| Token lifetime | 3600 seconds |
| Client provisioning | IAM portal |

---

## Subscription Management

| Operation | Method | Path |
|---|---|---|
| Create subscription | POST | `/subscriptions` |
| List subscriptions | GET | `/subscriptions?service_id={id}` |
| Get subscription | GET | `/subscriptions/{subscription_id}` |
| Delete subscription | DELETE | `/subscriptions/{subscription_id}` |
| Inspect DLQ | GET | `/subscriptions/{subscription_id}/dlq` |

**Maximum subscriptions per service:** 200  
**Minimum secret length:** 16 characters

---

## Delivery Contract

| Parameter | Value |
|---|---|
| Delivery method | HTTP POST |
| Protocol | HTTPS only |
| Response timeout | 10 seconds |
| Success codes | 2xx |
| Signature header | `X-EventBridge-Signature` |
| Signature algorithm | HMAC-SHA256 |

---

## Retry Policy and Dead Letter Queue

| Parameter | Value |
|---|---|
| DLQ threshold | 3 consecutive delivery failures |
| Retry attempts | 3 |
| Retry schedule | Fixed — 60 seconds between attempts |
| DLQ retention | 14 days |
| Automated replay | Not available — manual only |

Note: The retry schedule differs from PiSync's fixed 60-second interval in that
EventBridge uses exponential backoff. See the full spec for the backoff schedule.
(The table above shows legacy PiSync retry values for comparison.)

---

## Rate Limits

| Plan | Limit |
|---|---|
| Default | 1200 events/min per subscription |
| Legacy migration period | 1000 events/min (pre-November 1) |

Rate limits are returned in response headers:
`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## OAuth Scopes

| Scope | Required for |
|---|---|
| `eventbridge:write` | Create, update, delete subscriptions |
| `eventbridge:read` | List and inspect subscriptions |

---

## Topics

| Topic | Description |
|---|---|
| `account.created` | New account registered |
| `account.updated` | Account fields modified |
| `account.status_changed` | Account suspended, reactivated, or closed |
| `billing.invoice_issued` | Invoice generated |
| `billing.payment_received` | Payment processed |
| `risk.alert_raised` | Fraud or anomaly alert |
| `partner.event` | Partner-facing event envelope |

Wildcards: family-level only (e.g. `account.*`). Global `*` not supported.

---

## PiSync → EventBridge Field Mapping

| PiSync field | EventBridge equivalent |
|---|---|
| `service_name` | `service_id` |
| `event_type` | `topic` |
| `target_url` | `endpoint_url` |
| `signing_secret` | `secret` |
| `webhook_id` | `subscription_id` |
| `X-PiSync-Signature` | `X-EventBridge-Signature` |

---

*For questions: #platform-eng*

