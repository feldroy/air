from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dashboard import router
else:
    from dashboard import router

import air

app = air.Air()
app.include_router(router)


@app.page
def index() -> air.BaseTag:
    return air.layouts.mvpcss(air.H1("Avatar Data"), air.P(air.A("Dashboard", href="/dashboard")))
