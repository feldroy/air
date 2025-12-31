# This example turns on OpenAPI docs while continuing mostly normal Air behaviors.
# Go to 127.0.0.1:8000/docs or 127.0.0.1:8000/redoc
# This can be very useful for larger projects with many routes.
from fastapi import FastAPI

import air

fastapi_app = FastAPI(default_response_class=air.AirResponse, title="Air using OpenAPI to list routes.")
app = air.Air(fastapi_app=fastapi_app)


@app.page
def index() -> air.BaseTag:
    """Project home page

    Returns:

        air.BaseTag

    """
    return air.layouts.mvpcss(air.H1("Hello world"))


@app.page
def about() -> air.BaseTag:
    """This is the about page

    Returns:

        air.BaseTag
    """
    return air.layouts.mvpcss(air.H1("About air"))
