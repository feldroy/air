from fastapi.exceptions import HTTPException as FASTAPIHTTPException


class HTTPException(FASTAPIHTTPException):
    """Convenience import from FastAPI"""


class BaseAirException(Exception):
    """Base AIR Exception"""


class RenderException(BaseAirException):
    """Error thrown when render function fails."""


class ObjectDoesNotExist(HTTPException):
    """Thrown when a record in a persistence store can't be found."""
