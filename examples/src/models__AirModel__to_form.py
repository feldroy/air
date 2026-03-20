from collections.abc import Sequence

from airmodel import AirModel

import air
from air import AirForm
from air.forms import default_form_widget

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
    includes: Sequence[str] | None = None,
) -> air.Div:
    return air.Div(
        air.P("Custom form styling:"),
        air.Raw(default_form_widget(model=model, data=data, errors=errors, includes=includes)),
        class_="custom-form",
    )


class ContactForm(AirForm[ContactModel]):
    includes = ("name", "email")  # Only render these fields
    widget = custom_widget


@app.page
def index() -> air.Html:
    contact_form = ContactForm()
    return air.Html(
        air.H1("Contact Form"),
        air.P("This form demonstrates includes and widget parameters"),
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

    if contact_form.validate(dict(form_data)):
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
