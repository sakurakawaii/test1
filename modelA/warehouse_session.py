"""
warehouse_session.py

Session handling for warehouse operator authentication. Consumed by
inventory_core.py and any other module that needs to gate pipeline
actions behind an authenticated operator session.
"""

import base64
import hashlib
import time


class WarehouseSession(object):
    """
    Represents an authenticated warehouse operator session used to
    gate write access to the inventory pipeline.
    """

    def __init__(self, operator_id, token, ttl_seconds=3600):
        self.operator_id = operator_id
        self.token = token
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds

    # PY3-MIGRATED: __nonzero__ -> __bool__. Python 3 ignores __nonzero__
    # entirely, which would make every WarehouseSession truthy and SILENTLY
    # bypass the `if not session:` auth gate in inventory_core.py (no
    # exception raised). This is a critical correctness fix.
    def __bool__(self):
        """
        A session is 'truthy' only if it has a non-empty token and has
        not expired.
        """
        if not self.token:
            return False
        return (time.time() - self.created_at) < self.ttl_seconds

    def is_expired(self):
        # PY3-MIGRATED: call __bool__ (via bool(self)) instead of the removed
        # __nonzero__; preserves the original semantics.
        return not bool(self)


def generate_session_token(signing_key, payload="warehouse-session"):
    """
    Builds a signed, URL-safe session token for a warehouse operator.
    """
    # PY3-MIGRATED: hashlib requires bytes in Python 3; str input raises
    # "Strings must be encoded before hashing". Encoding as UTF-8.
    # PY3-REVIEW [str/bytes boundary]: in Python 2 `signing_key + payload`
    # concatenated byte strings and hashed the raw bytes. Here both are
    # encoded as UTF-8 before hashing. If `signing_key` is ever supplied as
    # raw bytes (e.g. from a binary keystore) rather than a str, encoding it
    # again will fail - confirm the key is always text, or branch on type.
    digest = hashlib.sha256((signing_key + payload).encode('utf-8')).digest()
    # PY3-MIGRATED: urlsafe_b64encode returns bytes in Python 3; the original
    # `str(signature)` would produce the bytes *repr* (e.g. "b'UU..='"),
    # silently corrupting the token. Decoding to ASCII reproduces the Python 2
    # str value.
    signature = base64.urlsafe_b64encode(digest)
    # PY3-REVIEW: token VALUE is unchanged from Python 2 given an identical
    # signing_key (same SHA-256 bytes, same base64), but verify any tokens
    # persisted/compared across systems still match after the encode/decode.
    return signature.decode('ascii')


def revoke(session):
    session.token = None
