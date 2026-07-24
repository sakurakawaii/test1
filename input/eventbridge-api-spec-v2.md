# EventBridge API — v2 Specification

**Status:** Approved — Current  
**Owner:** Platform Engineering (#platform-eng)  
**Last Updated:** 2026-07-20  
**Version:** 2.0.1

---

## Overview

EventBridge is the internal event delivery platform replacing PiSync. It provides reliable, ordered webhook delivery from Pitaron's core services to internal consumers. v2 consolidates what used to be three separate delivery mechanisms (`pisync-webhooks`, `internal-relay`, and the ad-hoc notification queue from the monolith) into a single subscription model centered on `subscription_id`.

If you are building a new integration, start here. If you are migrating from PiSync, see the Deprecated Endpoints section and the companion migration guide. The archived PiSync v1 specification is preserved in the docs archive for reference but **should not be used as a technical guide for EventBridge integrations** — field names, endpoint paths, and validation mechanics have changed materially.

---

## Authentication

All calls to the EventBridge management API must authenticate using OAuth2 client credentials. API key authentication is not supported by EventBridge.

```
POST https://auth.pitaron.io/oauth/token
Content-Type: application/x-www-form-urlencoded
grant_type=client_credentials
&client_id={client_id}
&client_secret={client_secret}
&scope=eventbridge:read eventbridge:write
```

Tokens expire after 3600 seconds. Use the `pitaron-auth-client` (v2.4+) for automatic refresh. If your service uses a non-JVM runtime, see the OAuth2 onboarding guide in the Platform Eng wiki for language-specific patterns.

---

## Endpoints

### POST /subscriptions

Creates a new event subscription. This is the canonical way to register a receiving endpoint with EventBridge.

**Request body**

```json
{
  "service_id": "billing-sync",
  "topic": "account.updated",
  "endpoint_url": "https://billing-sync.pitaron.internal/webhooks/account",
  "secret": "your-hmac-secret-minimum-32-chars"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| service_id | string | Yes | Your service's registered identifier in the service registry |
| topic | string | Yes | Event topic to subscribe to. Wildcard (`*`) supported for topic families only. |
| endpoint_url | string | Yes | HTTPS only. Must be reachable from the EventBridge delivery network. |
| secret | string | Yes | Used to compute the HMAC-SHA256 signature on delivery. Min 32 characters. |

**Example response — 201 Created**

```json
{
  "subscription_id": "sub_9a1f3c22-4d8e-4b1a-a901-33cf7d2e1b04",
  "service_id": "billing-sync",
  "topic": "account.updated",
  "endpoint_url": "https://billing-sync.pitaron.internal/webhooks/account",
  "status": "active",
  "created_at": "2026-07-20T09:14:00Z"
}
```

**Error responses**

| Status | Code | Notes |
|---|---|---|
| 400 | validation_error | Missing required fields, invalid topic format, or endpoint not reachable |
| 401 | unauthorized | Missing or expired token |
| 403 | insufficient_scope | Token lacks eventbridge:write |
| 409 | duplicate_subscription | Subscription for this service_id + topic + endpoint_url combination already exists |

A service may hold a maximum of **200 active subscriptions**. Attempts to create more will return `400 subscription_limit_exceeded`.

---

### GET /subscriptions

Lists all subscriptions for a given service.

**Query parameters**

| Name | Type | Required | Description |
|---|---|---|---|
| service_id | string | Yes | Filter by service |
| topic | string | No | Filter by topic |
| status | string | No | active, paused, errored |

---

### GET /subscriptions/{subscription_id}

Returns details for a single subscription, including current delivery status and error counts.

---

### DELETE /subscriptions/{subscription_id}

Deregisters a subscription. In-flight deliveries will complete; no new events will be dispatched after acknowledgement.

---

### GET /subscriptions/{subscription_id}/dlq

Returns events currently held in the Dead Letter Queue for this subscription. Events are retained for 14 days before expiry.

---

## Webhook Delivery

### Event shape

```json
{
  "event_id": "evt_3b2a1d9c-0011-4e44-b901-6ff1c2d3e4a5",
  "topic": "account.updated",
  "payload": { ... },
  "timestamp": "2026-07-20T09:14:33Z",
  "version": "2"
}
```

Events are delivered via HTTP POST to the `endpoint_url` registered on the subscription. Your endpoint must return a 2xx status within 10 seconds; any other response or a timeout is treated as a delivery failure.

### Signature validation

Every delivery request includes a signature header:

```
X-EventBridge-Signature: sha256=3b4c1d...
```

Validate by computing HMAC-SHA256 of the raw request body using the `secret` specified at subscription creation time, then comparing to the value in `X-EventBridge-Signature`. Do not use the `X-PiSync-Signature` header — that was the legacy signing mechanism and is not present on EventBridge deliveries.

Example (Python):

```python
import hmac, hashlib

def validate(body_bytes, secret, header_value):
    expected = "sha256=" + hmac.new(
        secret.encode(), body_bytes, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, header_value)
```

### Retry and Dead Letter Queue policy

If delivery fails, EventBridge retries with exponential backoff:

| Attempt | Delay |
|---|---|
| 1 (initial) | — |
| 2 | 30 seconds |
| 3 | 2 minutes |
| 4 | 10 minutes |
| 5 | 30 minutes |

After **5 consecutive failed delivery attempts**, the event is moved to the subscription's Dead Letter Queue. No further delivery is attempted automatically. Events in the DLQ can be replayed manually via the `GET /subscriptions/{subscription_id}/dlq` endpoint (replay support is on the roadmap; manual replay is currently the only path).

**Note:** Early documentation drafts incorrectly stated the DLQ threshold as 3 attempts. The correct threshold has always been 5. The v2.1 release notes address this discrepancy explicitly.

---

## Rate Limits

Default delivery rate: **1000 events/min per subscription**. This reflects the gateway capacity confirmed at v2.0 launch.

A temporary elevated limit of 1200 events/min is available during the PiSync migration window (through 2026-12-31) for services running EventBridge and PiSync in parallel. This elevation is not automatic — request it in #platform-eng. The elevated limit will revert to 1000 on 2027-01-01.

Rate limits are returned in response headers on all management API calls:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1753013400
```

---

## Topics

| Topic | Description | Triggered by |
|---|---|---|
| account.created | New account registered | accounts-svc |
| account.updated | Account fields modified | accounts-svc |
| account.status_changed | Account suspended, reactivated, or closed | accounts-svc |
| billing.invoice_issued | Invoice generated for an account | billing-svc |
| billing.payment_received | Payment successfully processed | billing-svc |
| risk.alert_raised | Fraud or anomaly alert from risk engine | risk-svc |
| partner.event | Generic partner-facing event envelope | partner-relay |

Topic wildcards: `account.*` matches all account topics. Full wildcard `*` is not supported.

---

## Deprecated: PiSync Compatibility Notes

PiSync subscriptions registered via `POST /webhooks/register` (the legacy endpoint) continue to receive events through the PiSync compatibility shim. The shim is in **Maintenance** status — existing PiSync subscriptions still function, but new registrations via the old endpoint are rejected. The shim will enter **Deprecated** status on 2026-10-01 with planned removal on **2026-12-31**.

All new subscriptions must use `POST /subscriptions` as documented above.

---

## Changelog

- **2.0.1** (2026-07-20): Clarified DLQ threshold wording. Added note on X-PiSync-Signature header deprecation. Minor editorial fixes.
- **2.0.0** (2026-04-22): Initial EventBridge v2 release. Consolidates pisync-webhooks, internal-relay, and monolith notification queue.

