"""
This project requires the "pyinstrument" package, intentionally not
included in the dependencies of the Air project.

Call pyinstrument by adding '?profile=1' after any URL
"""

from pyinstrument import Profiler

import air

app = air.Air()


@app.middleware("http")
async def profile_request(request: air.Request, call_next):
    profiling = request.query_params.get("profile", False)
    if profiling:
        profiler = Profiler()
        profiler.start()
        await call_next(request)
        profiler.stop()
        return air.api.responses.HTMLResponse(profiler.output_html())
    return await call_next(request)


@app.page
def index():
    return air.layouts.mvpcss(air.H1("Home"), air.Ol(*[air.Li(x) for x in range(1, 100)]))
