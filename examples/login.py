from fastapi import Depends
import air

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")

login_manager = air.LoginManager(login_url="/login")


@login_manager.user_loader
def load_user(user_id: str):
    # Replace with real DB lookup
    if user_id == "42":
        return {"id": 42, "name": "Alice"}
    return None


@app.get("/login")
async def login_page():
    # Example login page
    return air.layouts.mvpcss(
        air.H1("Login"),
        air.Form(
            air.Input(type="text", name="username"),
            air.Input(type="password", name="password"),
            air.Button("Login"),
            action="/do-login",
            method="post"
        ),
    )


@app.post("/do-login")
async def do_login(request: air.Request):
    # Example login logic
    form = await request.form()
    user_id = "42"  # hardcoded for example
    return await login_manager.login_user(request, user_id, redirect_url="/")


@app.get("/")
async def index(user=Depends(login_manager)):
    # If user not logged in, they get redirected
    return air.layouts.mvpcss(
        air.H1(f"Hello {user['name']}!"),
        air.A("Logout", href="/logout")
    )


@app.get("/logout")
async def do_login(request: air.Request):
    await login_manager.logout_user(request)
    return air.RedirectResponse(url="/", status_code=302)
