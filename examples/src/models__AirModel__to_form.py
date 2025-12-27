from collections.abc import Sequence

from pydantic import BaseModel

import air
from air.forms import default_form_widget

app = air.Air()


class ContactModel(air.AirModel):
    name: str
    email: str
    phone: str | None = None


def custom_widget(
    model: type[BaseModel],
    data: dict | None = None,
    errors: list | None = None,
    includes: Sequence[str] | None = None,
) -> air.Div:
    return air.Div(
        air.P("Custom form styling:"),
        air.Raw(default_form_widget(model, data, errors, includes)),
        class_="custom-form",
    )


def get_contact_form() -> air.AirForm:
    return ContactModel.to_form(
        name="CustomContactForm",  # Custom form class name
        includes=["name", "email"],  # Only render these fields
        widget=custom_widget,  # Custom rendering function
    )


@app.page
def index() -> air.Html:
    contact_form = get_contact_form()
    return air.Html(
        air.H1("Contact Form"),
        air.P("This form demonstrates name, includes, and widget parameters"),
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
    contact_form = get_contact_form()

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
