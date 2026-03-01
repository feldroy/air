"""Shared CSRF utilities for Air middleware and template helpers."""

from __future__ import annotations

import secrets
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from air.requests import Request
    from starlette.types import Scope

DEFAULT_CSRF_COOKIE_NAME = "air_csrf_token"
DEFAULT_CSRF_HEADER_NAME = "X-CSRF-Token"
DEFAULT_CSRF_FORM_FIELD_NAME = "csrf_token"

CSRF_STATE_TOKEN_KEY = "csrf_token"
CSRF_STATE_COOKIE_NAME_KEY = "csrf_cookie_name"
CSRF_STATE_FORM_FIELD_NAME_KEY = "csrf_form_field_name"


def new_csrf_token() -> str:
    """Generate a secure CSRF token."""
    return secrets.token_urlsafe(32)


def set_csrf_state(scope: Scope, *, token: str, cookie_name: str, form_field_name: str) -> None:
    """Attach CSRF data to request state for downstream consumers."""
    state = scope.setdefault("state", {})
    state[CSRF_STATE_TOKEN_KEY] = token
    state[CSRF_STATE_COOKIE_NAME_KEY] = cookie_name
    state[CSRF_STATE_FORM_FIELD_NAME_KEY] = form_field_name


def _get_request_state_attr(request: Request, attr: str) -> Any:
    try:
        return getattr(request.state, attr)
    except AttributeError:
        return None


def get_csrf_cookie_name_from_request(request: Request) -> str:
    """Get the active CSRF cookie name for a request."""
    cookie_name = _get_request_state_attr(request, CSRF_STATE_COOKIE_NAME_KEY)
    if isinstance(cookie_name, str):
        return cookie_name
    return DEFAULT_CSRF_COOKIE_NAME


def get_csrf_form_field_name_from_request(request: Request) -> str:
    """Get the active CSRF form field name for a request."""
    form_field_name = _get_request_state_attr(request, CSRF_STATE_FORM_FIELD_NAME_KEY)
    if isinstance(form_field_name, str):
        return form_field_name
    return DEFAULT_CSRF_FORM_FIELD_NAME


def get_csrf_token_from_request(request: Request) -> str:
    """Resolve CSRF token from request state or cookie.

    Raises:
        RuntimeError: If token is unavailable, typically because CSRFMiddleware is not installed.
    """
    token = _get_request_state_attr(request, CSRF_STATE_TOKEN_KEY)
    if isinstance(token, str):
        return token

    cookie_name = get_csrf_cookie_name_from_request(request)
    cookie_token = request.cookies.get(cookie_name)
    if isinstance(cookie_token, str):
        return cookie_token

    msg = "CSRF token not found on request. Add air.CSRFMiddleware before using csrf helpers."
    raise RuntimeError(msg)
