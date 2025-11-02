"""Example of using Air.post decorator."""

from pydantic import BaseModel

import air


class UserCreate(BaseModel):
    """User creation model."""

    name: str
    email: str


app = air.Air()


@app.post("/submit")
def submit_form():
    """Simple POST endpoint."""
    return air.Div(
        air.H2("Form Submitted!"),
        air.P("Thank you for your submission"),
    )


@app.post("/users")
def create_user(user: UserCreate):
    """POST endpoint with request body."""
    return air.Div(
        air.H2("User Created"),
        air.P(f"Name: {user.name}"),
        air.P(f"Email: {user.email}"),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
