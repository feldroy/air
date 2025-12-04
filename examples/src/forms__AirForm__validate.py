import air

app = air.Air()


class FlightModel(air.AirModel):
    flight_number: str
    destination: str


@app.post("/flight")
async def submit_flight(request: air.Request) -> air.Html:
    form_data = await request.form()
    flight_form = FlightModel.to_form()

    if flight_form.validate(form_data):
        # Form is valid
        return air.Html(
            air.H1("Flight Submitted"),
            air.P(f"Flight: {flight_form.data.flight_number}"),
            air.P(f"Destination: {flight_form.data.destination}"),
        )

    # Form has errors
    return air.Html(
        air.H1("Validation Failed"),
        air.P(f"Errors: {len(flight_form.errors or [])}"),
    )
