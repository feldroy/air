"""Example of using Air.get decorator."""

import air

app = air.Air()


@app.get("/hello")
def hello_world():
    """Simple GET endpoint returning HTML."""
    return air.H1("Hello, World!")


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """GET endpoint with path parameter."""
    return air.Div(
        air.H2(f"User ID: {user_id}"),
        air.P("This is a user profile page"),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
