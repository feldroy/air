from __future__ import annotations

from fastapi.exceptions import HTTPException as HTTPException


class BrowserOpenError(RuntimeError):
    """Opening the browser failed."""
