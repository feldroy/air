from __future__ import annotations

from typing import Final, Literal

from fastapi.datastructures import Default
from fastapi.utils import generate_unique_id

from .responses import AirResponse, JSONResponse

# Public default so apps/routers can import the same sentinel (meaning: special marker)
default_html_response: Final = Default(AirResponse)
default_json_response: Final = Default(JSONResponse)
default_generate_unique_id: Final = Default(generate_unique_id)


def compute_page_path(endpoint_name: str, separator: Literal["/", "-"] = "-") -> str:
    """index -> '/', otherwise '/name-with-dashes'."""
    return "/" if endpoint_name == "index" else f"/{endpoint_name.replace('_', separator)}"
