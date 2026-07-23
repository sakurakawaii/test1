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

    def __bool__(self):  # PY3-MIGRATED: __nonzero__ is ignored in Python 3; renamed to __bool__
        """
        A session is 'truthy' only if it has a non-empty token and has
        not expired.
        """
        # PY3-REVIEW: This truthiness hook gates `if not session:` in
        # inventory_core.py. If it is not named __bool__ in Python 3, instances
        # are always truthy and the auth guard silently never fires. Verified the
        # rename is consistent with the is_expired() caller below.
        if not self.token:
            return False
        return (time.time() - self.created_at) < self.ttl_seconds

    def is_expired(self):
        return not bool(self)  # PY3-MIGRATED: explicit self.__nonzero__() call -> bool(self)


def generate_session_token(signing_key, payload="warehouse-session"):
    """
    Builds a signed, URL-safe session token for a warehouse operator.
    """
    # PY3-MIGRATED: hashlib requires bytes in Python 3; str concatenation must be
    # encoded. For ASCII signing keys this reproduces the Python 2 digest exactly.
    # PY3-REVIEW: If signing_key may contain non-ASCII characters, the utf-8 bytes
    # differ from the raw byte string Python 2 hashed; confirm the key is ASCII.
    digest = hashlib.sha256((signing_key + payload).encode('utf-8')).digest()  # PY3-MIGRATED: encode str before hashing
    signature = base64.urlsafe_b64encode(digest)
    # PY3-MIGRATED: base64 returns bytes in Python 3. The original str(signature)
    # would produce the literal "b'...'" repr (a corrupted token); decode instead.
    return signature.decode('ascii')  # PY3-MIGRATED: str(bytes) -> bytes.decode('ascii')


def revoke(session):
    session.token = None
