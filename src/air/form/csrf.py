"""CSRF protection for AirForm.

Tokens are HMAC-signed with a process-global secret. No configuration is
needed for single-process deployments. For multi-process production, set
the AIRFORM_SECRET environment variable to at least 32 unpredictable bytes or call
``configure_csrf_secret()`` so every process uses the same secret.

Token format: timestamp:nonce:signature
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import sys
import time
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

if TYPE_CHECKING:
    from air.requests import Request


_MIN_SECRET_BYTES = 32
_MAX_TOKEN_LENGTH = 256


def _validate_secret(secret: bytes) -> bytes:
    """Require enough key material for HMAC-SHA-256.

    Raises:
        ValueError: If the secret contains fewer than 32 bytes.
    """
    if not secret:
        msg = "CSRF secret must not be empty."
        raise ValueError(msg)
    if len(secret) < _MIN_SECRET_BYTES:
        msg = f"CSRF secret must be at least {_MIN_SECRET_BYTES} bytes."
        raise ValueError(msg)
    return secret


def _initial_secret() -> bytes | None:
    """Load the configured secret or safely initialize a process-local one."""
    configured_secret = os.environ.get("AIRFORM_SECRET")
    if configured_secret is not None:
        return _validate_secret(configured_secret.encode())
    if sys.platform == "emscripten":
        return None
    return secrets.token_bytes(32)


#: Secret key for signing CSRF tokens. Threaded runtimes generate it eagerly
#: to avoid first-use races. Emscripten runtimes generate it on first use.
_SECRET: bytes | None = _initial_secret()

#: How long a CSRF token stays valid (seconds). Default: 1 hour.
CSRF_MAX_AGE: int = 3600

#: Name of the hidden input field in the form.
CSRF_FIELD_NAME: str = "csrf_token"


def configure_csrf_secret(secret: str | bytes) -> None:
    """Configure the secret used to sign and validate CSRF tokens.

    Use this when the runtime supplies secrets through an API other than
    environment variables. Configure the same non-empty secret in every process
    before rendering or validating forms. Replacing it later invalidates tokens
    signed with the previous secret.

    Args:
        secret: A text or byte secret containing at least 32 bytes.

    Raises:
        TypeError: If ``secret`` is not text or bytes.
        ValueError: If ``secret`` contains fewer than 32 bytes.
    """  # noqa: DOC502
    if isinstance(secret, str):
        normalized_secret = secret.encode()
    elif isinstance(secret, bytes):
        normalized_secret = secret
    else:
        msg = "CSRF secret must be str or bytes."
        raise TypeError(msg)
    _validate_secret(normalized_secret)

    global _SECRET
    _SECRET = normalized_secret


def generate_csrf_token() -> str:
    """Generate a signed CSRF token."""
    timestamp = str(int(time.time()))
    nonce = secrets.token_urlsafe(16)
    payload = f"{timestamp}:{nonce}"
    sig = hmac.new(_get_secret(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def _check_csrf_token(token: str, max_age: int = CSRF_MAX_AGE) -> str:
    """Validate a CSRF token string. Returns the token if valid.

    Raises:
        ValueError: If the token is missing, tampered, or expired.
    """
    if not isinstance(token, str) or len(token) > _MAX_TOKEN_LENGTH:
        msg = "Invalid CSRF token."
        raise ValueError(msg)

    parts = token.split(":")
    if len(parts) != 3:
        msg = "Invalid CSRF token."
        raise ValueError(msg)

    timestamp_str, nonce, sig = parts

    expected_payload = f"{timestamp_str}:{nonce}"
    expected_sig = hmac.new(_get_secret(), expected_payload.encode(), hashlib.sha256).hexdigest()
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


def _url_origin(url: str, *, allow_path: bool) -> tuple[str, str, int] | None:
    """Return a normalized HTTP origin, or None for malformed input."""
    if any(char.isspace() for char in url):
        return None
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme not in {"http", "https"}
        or hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or (not allow_path and (parsed.path or parsed.query))
    ):
        return None
    if port is None:
        port = 443 if parsed.scheme == "https" else 80
    return parsed.scheme, hostname, port


def _check_csrf_origin(request: Request) -> None:
    """Require a browser submission to originate from the request target.

    Raises:
        ValueError: If the source origin is missing, malformed, or different.
    """
    target_origin = _url_origin(str(request.url), allow_path=True)
    origin_headers = request.headers.getlist("origin")
    if origin_headers:
        source_origin = _url_origin(origin_headers[0], allow_path=False) if len(origin_headers) == 1 else None
    else:
        referer_headers = request.headers.getlist("referer")
        source_origin = _url_origin(referer_headers[0], allow_path=True) if len(referer_headers) == 1 else None

    if source_origin is None or target_origin is None or source_origin != target_origin:
        msg = "CSRF source origin does not match the request origin."
        raise ValueError(msg)


def _get_secret() -> bytes:
    """Return the configured secret, generating a process-local one on first use."""
    global _SECRET
    if _SECRET is None:
        _SECRET = secrets.token_bytes(32)
    return _SECRET


def csrf_hidden_input() -> tuple[str, str]:
    """Render a hidden input with a fresh CSRF token.

    Returns:
        A (html, token) tuple. The html is the hidden input element,
        the token is the raw value for storing on the form instance.
    """
    token = generate_csrf_token()
    html = f'<input type="hidden" name="{CSRF_FIELD_NAME}" value="{token}">'
    return html, token
