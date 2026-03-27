# Forms & validation

Built on Pydantic's `BaseModel`, the `AirForm` class validates data from HTML forms with type-safe access to the validated result.

<!-- blacken-docs:off -->
```python
from airmodel import AirModel

import air
from air import AirForm

app = air.Air()


class FlightModel(AirModel):
    flight_number: str
    destination: str


class FlightForm(AirForm[FlightModel]):
    pass


@app.page
async def index():
    return air.layouts.mvpcss(
        air.H1("Flight Form"),
        air.Form(
            air.Input(name="flight_number", placeholder="flight number"),
            air.Input(name="destination", placeholder="destination"),
            air.Button("Submit", type_="submit"),
            method="post",
            action="/flight-info",
        ),
    )


@app.post("/flight-info")
async def flight_info(request: air.Request):
    flight = await FlightForm.from_request(request)
    if flight.is_valid:
        return air.Html(
            air.H1(f"{flight.data.flight_number} → {flight.data.destination}")
        )

    # Show form with enhanced error messages and preserved user input
    return air.layouts.mvpcss(
        air.H1("Flight Form"),
        air.P("Please correct the errors below:"),
        air.Form(
            flight.render(),  # Automatically shows user-friendly error messages
            air.Button("Submit", type_="submit"),
            method="post",
            action="/flight-info",
        ),
    )
```
<!-- blacken-docs:on -->

## Enhanced Form Features

### User-Friendly Error Messages

Air Forms automatically convert technical Pydantic validation errors into clear, actionable messages:

```python
# Instead of: "Input should be a valid integer, unable to parse string as an integer"
# Users see: "Please enter a valid number."

# Instead of: "Field required"
# Users see: "This field is required."
```

### Value Preservation

When validation fails, user input is automatically preserved, so users don't have to re-enter their data:

```python
# User submits: {"flight_number": "AB123", "destination": ""}
# After validation error, the form still shows "AB123" in the flight_number field
flight = await FlightForm.from_request(request)
if not flight.is_valid:
    return show_form_with_errors(flight)  # Values are preserved automatically
```
