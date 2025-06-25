from fastapi import Header


def is_htmx_request(hx_request: str = Header(default=None)) -> bool:
    return hx_request is not None and hx_request.lower() == "true"
