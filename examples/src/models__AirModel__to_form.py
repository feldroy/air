import air
from air import AirForm, AirModel
from air.form import default_form_widget

app = air.Air()


class ContactModel(AirModel):
    name: str
    email: str
    phone: str | None = None


def custom_widget(
    *,
    model: type[AirModel],
    data: dict | None = None,
    errors: list | None = None,
    excludes: set[str] | None = None,
) -> air.Div:
    return air.Div(
        air.P("Custom form styling:"),
        air.Raw(default_form_widget(model=model, data=data, errors=errors, excludes=excludes)),
        class_="custom-form",
    )


class ContactForm(AirForm[ContactModel]):
    excludes = (("phone", "display"),)  # Don't render phone, but keep it in save_data
    widget = custom_widget


@app.page
def index() -> air.Html:
    contact_form = ContactForm()
    return air.Html(
        air.H1("Contact Form"),
        air.P("This form demonstrates excludes and widget parameters"),
        air.Form(
            contact_form.render(),
            air.Button("Submit", type_="submit"),
            method="post",
            action="/submit",
        ),
    )


@app.post("/submit")
async def submit(request: air.Request) -> air.Html:
    form_data = await request.form()
    contact_form = ContactForm()

    if contact_form.validate(form_data):
        return air.Html(
            air.H1("Success"),
            air.P(f"Name: {contact_form.data.name}"),
            air.P(f"Email: {contact_form.data.email}"),
        )

    return air.Html(
        air.H1("Error"),
        air.P(f"Errors: {len(contact_form.errors or [])}"),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
