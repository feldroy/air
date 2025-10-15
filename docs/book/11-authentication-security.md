# Authentication and Security

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

## Session Management

Air provides session middleware for managing user sessions:

```python
import secrets

# Create a secret key for signing sessions
SECRET_KEY = secrets.token_urlsafe(32)

# Add session middleware
app.add_middleware(
    air.SessionMiddleware,
    secret_key=SECRET_KEY
)

@app.get("/login")
def login_page():
    return air.layouts.mvpcss(
        air.Title("Login"),
        air.H1("Login"),
        air.Form(
            air.Label("Username", for_="username"),
            air.Input(type="text", name="username", id="username"),
            air.Label("Password", for_="password"),
            air.Input(type="password", name="password", id="password"),
            air.Button("Login", type="submit"),
            method="POST",
            action="/login"
        )
    )

@app.post("/login")
async def login(request: air.Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    # In real app, verify credentials against database
    if verify_credentials(username, password):
        # Set session data
        request.session["user_id"] = get_user_id(username)
        request.session["logged_in"] = True
        return air.RedirectResponse("/", status_code=303)
    else:
        return air.layouts.mvpcss(
            air.H1("Login Failed"),
            air.P("Invalid credentials. Please try again."),
            air.A("Try Again", href="/login")
        )

def require_login(func):
    """Decorator to require login for routes."""
    def wrapper(*args, **kwargs):
        request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, air.Request)), None)
        if not request or not request.session.get("logged_in"):
            return air.RedirectResponse("/login", status_code=303)
        return func(*args, **kwargs)
    return wrapper
```

## Password Hashing

Use a library like `passlib` for secure password handling:

```bash
uv add passlib[bcrypt]
```

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

## Cross-Site Request Forgery (CSRF) Protection

For production applications, implement CSRF protection:

```python
import secrets

def generate_csrf_token():
    return secrets.token_urlsafe(32)

@app.get("/form-with-csrf")
def form_with_csrf(request: air.Request):
    csrf_token = generate_csrf_token()
    request.session["csrf_token"] = csrf_token
    
    return air.layouts.mvpcss(
        air.Form(
            air.Input(type="hidden", name="csrf_token", value=csrf_token),
            air.Input(type="text", name="data"),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/process-data"
        )
    )
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add authentication and security features"
```