from __future__ import annotations

from fastapi.exceptions import HTTPException as FASTAPIHTTPException


class HTTPException(FASTAPIHTTPException):
    """Convenience import from FastAPI"""


class BaseAirException(Exception):
    """Base AIR Exception"""


class RenderException(BaseAirException):
    """Error thrown when a render function fails."""


class ObjectDoesNotExist(HTTPException):
    """Thrown when a record in a persistence store can't be found."""


class BrowserOpenError(RuntimeError):
    """Opening the browser failed."""
