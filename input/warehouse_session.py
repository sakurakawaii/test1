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

    def __nonzero__(self):
        """
        A session is 'truthy' only if it has a non-empty token and has
        not expired.
        """
        if not self.token:
            return False
        return (time.time() - self.created_at) < self.ttl_seconds

    def is_expired(self):
        return not self.__nonzero__()


def generate_session_token(signing_key, payload="warehouse-session"):
    """
    Builds a signed, URL-safe session token for a warehouse operator.
    """
    digest = hashlib.sha256(signing_key + payload).digest()
    signature = base64.urlsafe_b64encode(digest)
    return str(signature)


def revoke(session):
    session.token = None
