"""
Profile any page by adding '?profile=1' to the URL.

Requires the "pyinstrument" package (installed via the examples
dependency group: uv sync --group examples).
"""

from pyinstrument import Profiler
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

import air
from air import Children, Html

app = air.Air()


@app.middleware("http")
async def profile_request(request: air.Request, call_next: RequestResponseEndpoint) -> Response:
    profiling = request.query_params.get("profile", False)
    if profiling:
        profiler = Profiler()
        profiler.start()
        await call_next(request)
        profiler.stop()
        return air.responses.HTMLResponse(profiler.output_html())
    return await call_next(request)


@app.page
def index() -> Children | Html:
    return air.layouts.mvpcss(air.H1("Home"), air.Ol(*[air.Li(x) for x in range(1, 100)]))
