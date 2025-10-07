#!/usr/bin/env python3
"""Demo script to show enhanced form error messages."""

from pydantic import BaseModel, Field
from rich import print

import air


class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, le=120)  # Age between 1 and 120
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")  # Basic email pattern


class ContactForm(air.AirForm):
    model = ContactModel


app = air.Air()


@app.get("/")
async def show_form():
    """Show the form initially."""
    form = ContactForm()
    return air.layouts.picocss(
        air.Title("Enhanced Form Errors Demo"),
        air.H1("Contact Form - Error Message Demo"),
        air.Form(
            form.render(),
            air.Button("Submit", type="submit"),
            method="post",
            action="/submit",
        ),
    )


@app.post("/submit")
async def handle_form(request: air.Request):
    """Handle form submission and show errors."""
    form = await ContactForm.from_request(request)

    if form.is_valid:
        return air.layouts.picocss(
            air.Title("Success"),
            air.H1("Success!"),
            air.P(f"Name: {form.data.name}"),
            air.P(f"Age: {form.data.age}"),
            air.P(f"Email: {form.data.email}"),
        )

    # Show form with enhanced error messages
    return air.layouts.picocss(
        air.Title("Enhanced Form Errors Demo"),
        air.H1("Contact Form - With Enhanced Error Messages"),
        air.P("Notice the specific, user-friendly error messages below:"),
        air.Form(
            form.render(),
            air.Br(),
            air.Button("Submit", type="submit"),
            method="post",
            action="/submit",
        ),
        air.Hr(),
        air.Details(
            air.Summary("Technical Error Details (for developers)"),
            air.P(str(form.errors)) if form.errors else "No errors",
        ),
    )


if __name__ == "__main__":
    import uvicorn

    print("Demo server starting...")
    print("1. Open http://localhost:8000 in your browser")
    print("2. Leave fields empty and click Submit to see 'This field is required.'")
    print("3. Enter invalid data (like 'abc' for age) to see 'Please enter a valid number.'")
    uvicorn.run(app, host="127.0.0.1", port=8000)
