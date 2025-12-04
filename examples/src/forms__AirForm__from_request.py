import air

app = air.Air()


class FlightModel(air.AirModel):
    flight_number: str
    destination: str


FlightForm = FlightModel.to_form()


@app.post("/flight")
async def submit_flight(request: air.Request) -> air.Html:
    flight = await FlightForm.from_request(request)

    if flight.is_valid:
        # Form is valid
        return air.Html(
            air.H1("Flight Submitted"),
            air.P(f"Flight: {flight.data.flight_number}"),
            air.P(f"Destination: {flight.data.destination}"),
        )

    # Form has errors
    return air.Html(
        air.H1("Validation Failed"),
        air.P(f"Errors: {len(flight.errors or [])}"),
    )
