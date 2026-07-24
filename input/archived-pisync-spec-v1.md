# PiSync Webhook Delivery — v1 Specification

**Status:** Archived  
**Owner:** Platform Engineering  
**Last Updated:** 2025-09-30  
**Superseded by:** EventBridge API v2 (see `eventbridge-api-spec-v2.md`)

---

> **Note:** This document describes the PiSync v1 webhook system, which is no longer under active development. It is preserved for historical reference only. For current EventBridge specifications, consult `eventbridge-api-spec-v2.md`.

---

## Overview

PiSync provided webhook delivery for internal services from 2022 through mid-2026. It supports push-based event delivery to registered HTTP endpoints using a topic-based subscription model.

---

## Authentication

PiSync management API calls authenticate using an API key passed in the `X-Api-Key` request header:

```
X-Api-Key: psk_live_a93b4c11...
```

API keys are provisioned per service through the IAM portal.

---

## Registering a Subscription

```
POST https://pisync.pitaron.internal/webhooks/register
Content-Type: application/json
X-Api-Key: psk_live_a93b4c11...

{
  "service_name": "billing-sync",
  "event_type": "account.updated",
  "target_url": "https://billing-sync.pitaron.internal/hooks/incoming",
  "signing_secret": "your-secret"
}
```

Note: field names differ from EventBridge. PiSync uses `service_name`, `event_type`, and `target_url` rather than `service_id`, `topic`, and `endpoint_url`.

A successful registration returns a `webhook_id` (not a `subscription_id` — see naming differences section below).

---

## Webhook Delivery

Events are delivered via HTTP POST to the `target_url`. The request includes:

```
X-PiSync-Signature: sha256=7f3c1b...
X-PiSync-Event-Type: account.updated
X-PiSync-Delivery-Id: del_4b3a...
```

### Signature validation

Validate using HMAC-SHA256 of the raw body with your `signing_secret`, compared against the `X-PiSync-Signature` header:

```python
import hmac, hashlib

def validate_pisync(body_bytes, secret, header_value):
    expected = "sha256=" + hmac.new(
        secret.encode(), body_bytes, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, header_value)
```

---

## Retry Policy

PiSync retries failed deliveries (non-2xx or timeout) up to 3 times with a fixed 60-second delay between attempts. After 3 failures, the event is considered undeliverable and logged to the internal dead letter store. No automatic replay was provided — teams had to request replays through the PiSync admin tooling.

---

## Rate Limits

Default: 500 events/min per registered webhook. Custom limits were available on request through #platform-eng.

---

## Naming Differences vs EventBridge

| Concept | PiSync field | EventBridge equivalent |
|---|---|---|
| Subscription identifier | webhook_id | subscription_id |
| Service identifier | service_name | service_id |
| Event category | event_type | topic |
| Target URL | target_url | endpoint_url |
| Signature header | X-PiSync-Signature | X-EventBridge-Signature |

---

## Deprecation

PiSync is in Maintenance status. Existing subscriptions continue to receive events through the compatibility shim built into EventBridge. New registrations via `POST /webhooks/register` are no longer accepted — use `POST /subscriptions` on the EventBridge platform instead.

---

*End of archived document. For current integration guidance see `eventbridge-api-spec-v2.md`.*

