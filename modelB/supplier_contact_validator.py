"""
supplier_contact_validator.py

Validates supplier contact fields (name, email, phone) pulled from
onboarding forms before a supplier record is activated.
"""

import re

# PY3-MIGRATED: re.ASCII preserves Python 2 ASCII-only \w/\d/\s semantics.
# PY3-REVIEW: re.ASCII on EMAIL_PATTERN keeps Python 2 behavior but rejects
# internationalized (EAI / non-ASCII) email addresses. Confirm with onboarding
# whether international supplier emails must be accepted; drop re.ASCII if so.
EMAIL_PATTERN = re.compile(r'^[\w.\-]+@[\w.\-]+\.\w+$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w semantics
PHONE_PATTERN = re.compile(r'^\+?\d[\d\-\s]{7,14}\d$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \d/\s semantics
NAME_PATTERN = re.compile(r'^[A-Za-z\s.\-]+$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \s semantics
POSTAL_CODE_PATTERN = re.compile(r'^\w{3,10}$', re.ASCII)  # PY3-MIGRATED: re.ASCII preserves Py2 \w semantics


def is_valid_email(email):
    return bool(EMAIL_PATTERN.match(email))


def is_valid_phone(phone):
    return bool(PHONE_PATTERN.match(phone))


def is_valid_contact_name(name):
    parts = name.split()
    # PY3-REVIEW: str.isalpha() is Unicode-aware in Python 3, so accented supplier
    # names (e.g. "José") now pass isalpha() where they failed on Python 2 byte
    # strings. The re.ASCII NAME_PATTERN [A-Za-z] still rejects them, so the
    # combined result stays ASCII-only. If international names SHOULD be accepted,
    # relax both checks together rather than only one.
    return all(part.isalpha() for part in parts) and bool(NAME_PATTERN.match(name))


def is_valid_postal_code(code):
    return bool(POSTAL_CODE_PATTERN.match(code))
