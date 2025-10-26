"""
This project requires the "pyinstrument" package, intentionally not
included in the dependencies of the Air project.

Call pyinstrument by adding '?profile=1' after any URL
"""

from collections.abc import Awaitable, Callable

from pyinstrument import Profiler

import air
from air import Children, Html

app = air.Air()


@app.middleware("http")
async def profile_request(request: air.Request, call_next: Callable[[air.Request], Awaitable[air.responses.Response]]):
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
