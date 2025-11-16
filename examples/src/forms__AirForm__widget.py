import air
from air.forms import default_form_widget

app = air.Air()


class ContactModel(air.AirModel):
    # Note: This uses `str` for email. For stricter server-side validation,
    # you can use `EmailStr` from pydantic.
    name: str
    email: str
    message: str


def contact_widget(*, model, data, errors, includes):
    base_html = default_form_widget(
        model=model,
        data=data,
        errors=errors,
        includes=includes,
    )

    return air.Div(
        air.P("Custom widget wrapper"),
        air.Raw(base_html),
        class_="contact-form",
    )


def get_contact_form() -> air.AirForm:
    return ContactModel.to_form(widget=contact_widget)


@app.page
def contact(request: air.Request):

    form = get_contact_form()

    return air.layouts.mvpcss(
        air.H1("Contact Us"),
        air.P("This example uses a custom AirForm.widget to wrap the default form HTML."),
        air.Form(
            form.render(),
            air.Button("Send message", type="submit"),
            method="post",
            action="/contact",
        ),
    )


@app.post("/contact")
async def submit_contact(request: air.Request):
    form = get_contact_form()
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
            air.Button("Send message", type="submit"),
            method="post",
            action="/contact",
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
