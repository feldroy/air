from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

import air

app = air.Air()


class FlightModel(BaseModel):
    flight_number: str
    destination: str


class FlightForm(air.AirForm):
    model = FlightModel


@app.post("/flight")
async def flight_form(request: air.Request) -> air.Html:
    "Awaited form data"
    flight = await FlightForm.from_request(request)
    if flight.is_valid:
        return air.Html(air.H1(flight.data.flight_number))
    errors = len(flight.errors or [])
    return air.Html(air.H1(air.Raw(str(errors))))


@app.post("/flight-depends")
async def flight_form_depends(flight: Annotated[FlightForm, Depends(FlightForm.from_request)]) -> air.Html:
    "Dependency injection"
    if flight.is_valid:
        return air.Html(air.H1(flight.data.flight_number))
    errors = len(flight.errors or [])
    return air.Html(air.H1(air.Raw(str(errors))))
