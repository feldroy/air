import air
from air import AirForm, AirModel
from air.form import default_form_widget

app = air.Air()


class ContactModel(AirModel):
    # Note: This uses `str` for email. For stricter server-side validation,
    # you can use `EmailStr` from pydantic.
    name: str
    email: str
    message: str


def contact_widget(
    *,
    model: type[AirModel],
    data: dict | None = None,
    errors: list | None = None,
    excludes: set[str] | None = None,
) -> air.Div:

    base_html = default_form_widget(
        model=model,
        data=data,
        errors=errors,
        excludes=excludes,
    )

    return air.Div(
        air.P("Custom widget wrapper"),
        air.Raw(base_html),
        class_="contact-form",
    )


class ContactForm(AirForm[ContactModel]):
    widget = contact_widget


@app.page
def contact(request: air.Request) -> air.Html | air.Children:

    form = ContactForm()

    return air.layouts.mvpcss(
        air.H1("Contact Us"),
        air.P("This example uses a custom AirForm.widget to wrap the default form HTML."),
        air.Form(
            form.render(),
            air.Button("Send message", type_="submit"),
            method="post",
            action="/contact",
        ),
    )


@app.post("/contact")
async def submit_contact(request: air.Request) -> air.Html:
    form = ContactForm()
    form_data = await request.form()

    if form.validate(form_data):
        return air.Html(
            air.H1("Thank you for your message!"),
            air.P("Your contact form was submitted successfully."),
        )

    error_count = len(form.errors or [])
    return air.Html(
        air.H1("Please fix the errors below."),
        air.P(f"Found {error_count} validation error(s)."),
        air.Form(
            form.render(),
            air.Button("Send message", type_="submit"),
            method="post",
            action="/contact",
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
