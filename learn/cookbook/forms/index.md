# Forms & validation

Built on Pydantic's `BaseModel`, the `air.AirForm` class is used to validate data coming from HTML forms.

```
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

    # Show form with enhanced error messages and preserved user input
    return air.layouts.mvpcss(
        air.H1("Flight Form"),
        air.P("Please correct the errors below:"),
        air.Form(
            flight.render(),  # Automatically shows user-friendly error messages
            air.Button("Submit", type="submit"),
            method="post",
            action="/flight-info",
        ),
    )
```

## Enhanced Form Features

### User-Friendly Error Messages

Air Forms automatically convert technical Pydantic validation errors into clear, actionable messages:

```
# Instead of: "Input should be a valid integer, unable to parse string as an integer"
# Users see: "Please enter a valid number."

# Instead of: "Field required"
# Users see: "This field is required."
```

### Value Preservation

When validation fails, user input is automatically preserved, so users don't have to re-enter their data:

```
# User submits: {"flight_number": "AB123", "destination": ""}
# After validation error, the form still shows "AB123" in the flight_number field
flight = await FlightForm.from_request(request)
if not flight.is_valid:
    return show_form_with_errors(flight)  # Values are preserved automatically
```

## Coming Soon: Dependency-Injection Form Handling

It is possible to use dependency injection to manage form validation.

NOTE: This functionality is currently in development. This feature was working before but currently does not work.

```
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
