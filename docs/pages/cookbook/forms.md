# Forms & validation

Built on Pydantic's `BaseModel`, the `air.AirForm` class is used to validate data coming from HTML forms.

```python
from typing import Annotated
from fastapi import Depends, Request
from pydantic import BaseModel, Field
import air

app = air.Air()

class FlightModel(BaseModel):
    flight_number: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)

class FlightForm(air.AirForm):
    model = FlightModel

@app.page
async def index():
    return air.layouts.mvpcss(
        air.H1("Flight Form"),
        air.Form(
            air.Input(name="flight_number", placeholder='flight number'),
            air.Input(name="destination", placeholder='destination'),
            air.Button("Submit", type="submit"),
            method="post",
            action="/flight-info",
        ),
    )

@app.post("/flight-info")
async def flight_info(request: Request):
    flight = await FlightForm.from_request(request)
    if flight.is_valid:
        return air.Html(air.H1(f'{flight.data.flight_number} → {flight.data.destination}'))
    return air.Html(
        air.H1("Errors"),
        air.Ul(*[
            air.Li(f"{err['loc'][0]}: {err['msg']}")
            for err in flight.errors
        ])
    )
```

## Coming Soon: Dependency-Injection Form Handling

It is possible to use dependency injection to manage form validation.

NOTE: This functionality is currently in development. This feature was working before but currently does not work.

```python
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


@app.page
async def flight():
    return air.Html(
        air.H1("Flight Form"),
        air.Form(
            air.Input(name="flight_number"),
            air.Input(name="destination"),
            air.Button("Submit", type="submit"),
            method="post",
            action="/flight-info",
        ),
    )


@app.post("/flight-info")
async def flight_info(flight: Annotated[FlightForm, Depends(FlightForm.validate)]):
    if flight.is_valid:
        return air.Html(air.H1(f'{flight.data.flight_number} → {flight.data.destination}'))
    return air.Html(air.H1(f"Errors {len(flight.errors)}"))
```
