"""Tools for handling dependencies, for things like handling incoming data from client libraries like HTMX."""

from fastapi import Depends, Header


def _is_htmx_request(hx_request: str = Header(default=None)) -> bool:
    """Dependency injection function used to determine if request is coming from HTMX. Checks if 'hx-request' header is in the HTTP request.

    Returns:
        bool: Whether or not a request is coming from an HTMX action.

    Example:

        import air

        app = air.App()


        @app.get("/")
        def index_get(is_htmx: bool = air.is_htmx_request):
            return air.H1(f"Is HTMX request?: {is_htmx}")


        @app.post("/")
        def index_post(is_htmx: bool = air.is_htmx_request):
            return air.H1(f"Is HTMX request?: {is_htmx}")


        @app.patch("/")
        def index_patch(is_htmx: bool = air.is_htmx_request):
            return air.AirResponse(air.H1(f"Is HTMX request?: {is_htmx}"))


        @app.put("/")
        def index_put(is_htmx: bool = air.is_htmx_request):
            return air.AirResponse(air.H1(f"Is HTMX request?: {is_htmx}"))


        @app.delete("/")
        def index_delete(is_htmx: bool = air.is_htmx_request):
            return air.AirResponse(air.H1(f"Is HTMX request?: {is_htmx}"))
    """
    return hx_request is not None and hx_request.lower() == "true"


is_htmx_request = Depends(_is_htmx_request)
