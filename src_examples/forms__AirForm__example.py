"""Small examples for AirForm and AirField usage.

This file is intentionally minimal and used by tests (not executed as an application).
"""

from pydantic import BaseModel

from air.forms import AirField, AirForm
from air.requests import Request


class FlightModel(BaseModel):
    flight_number: str = AirField(label="Flight Number", autofocus=True, type="text")
    seats: int = AirField(type="number")


class FlightForm(AirForm):
    model = FlightModel


async def example_from_request(request: Request) -> FlightForm:
    """Awaited form example: returns an instance of FlightForm populated from request.form()."""
    # Return the validated FlightForm instance created from the request.
    return await FlightForm.from_request(request)
