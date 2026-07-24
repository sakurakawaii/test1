# PiSync → EventBridge Migration Guide

**Status:** DRAFT — internal only, not for distribution  
**Author:** Connor Marsh  
**Created:** 2026-05-01  
**Last edited:** 2026-05-28  

TODO: Needs review from Lena before publishing. Auth section especially — I'm not fully certain on the OAuth scopes for EventBridge vs PiSync.

---

## Overview

This guide covers what teams need to do to migrate their webhook integrations from PiSync to EventBridge. The EventBridge platform replaces PiSync's delivery infrastructure with a cleaner subscription model and improved retry guarantees.

The main things that change:

- Subscriptions are registered at a new endpoint (see Step 2 below)
- Signature validation uses a new HMAC header (see Step 3)
- Rate limits differ from PiSync defaults

This document assumes you have read the EventBridge spec. If you haven't, start there.

TODO: Link to the published spec once it's out of draft — I think Platform Eng is publishing it in the internal docs site soon.

---

## Who Needs to Migrate

If your service registers webhook subscriptions via PiSync's `POST /webhooks/register` endpoint, you need to migrate. Check the migration tracker (Sofia maintains it in the platform-eng shared drive) to see if your service has already been assessed.

---

## Migration Steps

### Step 1 — Audit your PiSync subscriptions

List your current PiSync subscriptions and note the topics and endpoint URLs. You'll need these when re-registering on EventBridge.

Check your service's config or environment variables for a `PISYNC_API_KEY` — if that's present, your service is definitely using PiSync.

### Step 2 — Register on EventBridge

Register your subscription by calling the EventBridge webhook registration endpoint:

```
POST https://eventbridge.pitaron.internal/webhooks/register
Content-Type: application/json
Authorization: Bearer {oauth_token}

{
  "service_id": "your-service-id",
  "topic": "account.updated",
  "endpoint_url": "https://your-service.pitaron.internal/hooks/incoming",
  "secret": "your-secret-for-hmac-signing"
}
```

TODO: I'm not 100% sure `webhooks/register` is the final path — need to confirm with James or Lena before publishing this. I pulled it from the early EventBridge design doc.

You'll get back a `subscription_id` — store this, you'll need it for any subsequent subscription management calls.

### Step 3 — Update signature validation

PiSync signed webhook payloads using an HMAC-SHA256 of the body with your secret, sent in the `X-PiSync-Signature` header. EventBridge uses the same HMAC-SHA256 approach, but the header name is different.

Update your validation code to read from `X-PiSync-Signature` instead of whatever you were using before.

TODO: Double-check the header name with Lena — I've seen `X-EventBridge-Sig` in some early docs too. Need to confirm which one shipped.

Example validation check:

```python
import hmac, hashlib

received = request.headers.get("X-PiSync-Signature")
expected = "sha256=" + hmac.new(
    secret.encode(), request.body, hashlib.sha256
).hexdigest()
assert hmac.compare_digest(expected, received)
```

### Step 4 — Adjust retry expectations

PiSync would retry a failed webhook delivery 3 times before giving up. EventBridge has a similar retry policy with the same 3-attempt threshold before the event is moved to the Dead Letter Queue.

If your service had logic that assumed at least 3 retries, that assumption still holds on EventBridge.

### Step 5 — Update authentication

PiSync subscriptions were managed using your team's API key in the `X-Api-Key` header. EventBridge uses OAuth2. You'll need credentials before you can register:

```
POST https://auth.pitaron.io/oauth/token
Content-Type: application/x-www-form-urlencoded
grant_type=client_credentials
&client_id={your_client_id}
&client_secret={your_client_secret}
&scope=eventbridge:read eventbridge:write
```

Request credentials through the IAM portal if you don't have them.

### Step 6 — Run in parallel and cut over

It's safe to have both PiSync and EventBridge subscriptions active simultaneously for a period. Run both during testing and switch off PiSync once you're satisfied EventBridge is delivering correctly.

### Step 7 — Remove your PiSync configuration

Once migrated, remove the `PISYNC_API_KEY` from your service config and delete your PiSync subscription if the PiSync management interface allows it (TODO: confirm whether PiSync has a deregistration endpoint — I don't think it ever did).

---

## Validation Checklist

- PiSync `POST /webhooks/register` call replaced with EventBridge registration
- Signature validation updated to use `X-PiSync-Signature` header
- Retry/DLQ expectations updated (threshold: 3 failed attempts)
- API Key removed from config, OAuth2 credentials in place
- Tested in staging with parallel delivery
- Migration tracker updated

---

## Common Issues

**Signature mismatch on delivery**
If your endpoint returns 401 or 403 on incoming events, check that you're reading the right header for the signature. If you previously validated `X-PiSync-Signature` on PiSync deliveries, the same header should work on EventBridge.

**Subscription not found after registration**
There was a caching delay in early EventBridge builds where a newly created subscription could take up to 60 seconds to appear in GET calls. This should be resolved in the current release, but worth knowing if you hit it in staging.

**Rate limit differences**
PiSync ran at 500 events/min. EventBridge's default is higher. Check the current EventBridge spec for exact numbers — I've seen a few different values floating around and I don't want to publish a wrong number here.

---

## References

- EventBridge spec — platform-eng docs (link TBD)
- PiSync v1 spec — archived in platform-eng/docs/legacy
- Migration tracker — Sofia, platform-eng shared drive
- IAM portal — internal wiki

