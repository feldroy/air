"""Zero-config CSRF protection for AirForm.

Tokens are HMAC-signed with a per-process secret that's auto-generated
on import. No configuration needed for single-worker deployments. For
multi-worker production, set the AIRFORM_SECRET environment variable
so all workers share the same secret.

Token format: timestamp:nonce:signature
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from typing import TYPE_CHECKING, Any

from pydantic_core import core_schema

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import CoreSchema

#: Secret key for signing CSRF tokens. Auto-generated per process,
#: or read from AIRFORM_SECRET env var for multi-worker deployments.
_SECRET: bytes = os.environ.get("AIRFORM_SECRET", "").encode() or secrets.token_bytes(32)

#: How long a CSRF token stays valid (seconds). Default: 1 hour.
CSRF_MAX_AGE: int = 3600

#: Name of the hidden input field in the form.
CSRF_FIELD_NAME: str = "csrf_token"


def generate_csrf_token() -> str:
    """Generate a signed CSRF token."""
    timestamp = str(int(time.time()))
    nonce = secrets.token_urlsafe(16)
    payload = f"{timestamp}:{nonce}"
    sig = hmac.new(_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def _check_csrf_token(token: str, max_age: int = CSRF_MAX_AGE) -> str:
    """Validate a CSRF token string. Returns the token if valid.

    Raises:
        ValueError: If the token is missing, tampered, or expired.
    """
    parts = token.split(":")
    if len(parts) != 3:
        msg = "Invalid CSRF token."
        raise ValueError(msg)

    timestamp_str, nonce, sig = parts

    expected_payload = f"{timestamp_str}:{nonce}"
    expected_sig = hmac.new(_SECRET, expected_payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_sig, sig):
        msg = "Invalid CSRF token."
        raise ValueError(msg)

    try:
        token_time = int(timestamp_str)
    except ValueError:
        msg = "Invalid CSRF token."
        raise

    if time.time() - token_time > max_age:
        msg = "CSRF token has expired. Please resubmit the form."
        raise ValueError(msg)

    return token


class ValidCsrfToken(str):  # noqa: FURB189
    """A Pydantic-native string type that validates CSRF token signatures.

    Used on the wrapper model that AirForm creates automatically.
    Pydantic validates it alongside all other fields, so CSRF errors
    appear in form.errors through the same machinery.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> str:
        if not isinstance(value, str):
            msg = "CSRF token must be a string."
            raise TypeError(msg)
        return _check_csrf_token(value)


def csrf_hidden_input() -> tuple[str, str]:
    """Render a hidden input with a fresh CSRF token.

    Returns:
        A (html, token) tuple. The html is the hidden input element,
        the token is the raw value for storing on the form instance.
    """
    token = generate_csrf_token()
    html = f'<input type="hidden" name="{CSRF_FIELD_NAME}" value="{token}">'
    return html, token
