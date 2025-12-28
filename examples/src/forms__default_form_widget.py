import air
from air.forms import default_form_widget

app = air.Air()


class FlightModel(air.AirModel):
    flight_number: str
    destination: str
    passengers: int


@app.page
def index(request: air.Request) -> air.Html:
    # Render different field groups separately using includes parameter
    basic_info = default_form_widget(
        model=FlightModel,
        data={"flight_number": "AA123"},  # Pre-populate flight_number
        includes=["flight_number", "destination"],
    )

    passenger_info = default_form_widget(
        model=FlightModel,
        includes=["passengers"],
    )

    return air.Html(
        air.H1("Flight Booking"),
        air.Form(
            air.Fieldset(
                air.Legend("Flight Information"),
                air.Raw(basic_info),
            ),
            air.Fieldset(
                air.Legend("Passenger Count"),
                air.Raw(passenger_info),
            ),
            air.Button("Submit", type_="submit"),
            method="post",
            action="/submit",
        ),
    )


@app.post("/submit")
async def submit(request: air.Request) -> air.Html:
    form_data = await request.form()
    flight_form = FlightModel.to_form()

    if flight_form.validate(form_data):
        return air.Html(
            air.H1("Flight Booked"),
            air.P(f"Flight: {flight_form.data.flight_number}"),
            air.P(f"Destination: {flight_form.data.destination}"),
            air.P(f"Passengers: {flight_form.data.passengers}"),
        )

    # Re-render with custom layout and errors
    basic_info = default_form_widget(
        model=FlightModel,
        data=dict(form_data),
        errors=flight_form.errors,
        includes=["flight_number", "destination"],
    )

    passenger_info = default_form_widget(
        model=FlightModel,
        data=dict(form_data),
        errors=flight_form.errors,
        includes=["passengers"],
    )

    return air.Html(
        air.H1("Please fix the errors"),
        air.Form(
            air.Fieldset(
                air.Legend("Flight Information"),
                air.Raw(basic_info),
            ),
            air.Fieldset(
                air.Legend("Passenger Count"),
                air.Raw(passenger_info),
            ),
            air.Button("Submit", type_="submit"),
            method="post",
            action="/submit",
        ),
    )
