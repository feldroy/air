from fastapi import FastAPI
from .responses import TagResponse


class Air(FastAPI):
    """FastAPI wrapper class with TagResponse as the default response class."""

    def __init__(self, *args, **kwargs):
        """Initialize Air app with TagResponse as default response class.

        Args:
            default_response_class: The default response class to use for endpoints.
                                  Defaults to TagResponse.
            *args: Additional positional arguments passed to FastAPI.
            **kwargs: Additional keyword arguments passed to FastAPI.
        """
        super().__init__(default_response_class=TagResponse, *args, **kwargs)
