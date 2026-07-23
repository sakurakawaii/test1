"""
supplier_contact_validator.py

Validates supplier contact fields (name, email, phone) pulled from
onboarding forms before a supplier record is activated.

PY3-REVIEW [MEDIUM - Unicode regex/str semantics]: No Python 2 syntax
constructs are present, so no lines were changed. In Python 3 str.isalpha()
is Unicode-aware (e.g. accented letters pass), while NAME_PATTERN stays
ASCII-only ([A-Za-z]); the combined result still rejects non-ASCII names,
but confirm this is intended for international suppliers. Phone/email/postal
inputs are expected ASCII.
"""

import re

EMAIL_PATTERN = re.compile(r'^[\w.\-]+@[\w.\-]+\.\w+$')
PHONE_PATTERN = re.compile(r'^\+?\d[\d\-\s]{7,14}\d$')
NAME_PATTERN = re.compile(r'^[A-Za-z\s.\-]+$')
POSTAL_CODE_PATTERN = re.compile(r'^\w{3,10}$')


def is_valid_email(email):
    return bool(EMAIL_PATTERN.match(email))


def is_valid_phone(phone):
    return bool(PHONE_PATTERN.match(phone))


def is_valid_contact_name(name):
    parts = name.split()
    return all(part.isalpha() for part in parts) and bool(NAME_PATTERN.match(name))


def is_valid_postal_code(code):
    return bool(POSTAL_CODE_PATTERN.match(code))
