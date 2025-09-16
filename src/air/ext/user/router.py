# """Authentication and authorization"""

# from datetime import datetime, timezone, timedelta
# import html
# from typing import Dict, Any
# import hashlib
# import json
# from os import getenv

# from cryptography.fernet import Fernet, InvalidToken
# import air
# from fastapi import status, Depends
# import pydantic
# from sqlmodel import select

# from .models import User, UserStatusEnum


# DOMAIN = getenv('DOMAIN', 'localhost:8000')
# FERNET_KEY = getenv("FERNET_KEY")
# if not FERNET_KEY:
#     raise ValueError("FERNET_KEY environment variable must be set for security")
# fernet = Fernet(FERNET_KEY.encode("utf-8") )


# # mailservice config
# # mg_key: str = getenv("MAILGUN_API_KEY", "")
# # email_client: MailgunClient = MailgunClient(auth=("api", mg_key))
# email_client = '1234'


# ## Utilities
# def require_auth(request: air.Request) -> Dict[str, Any]:
#     """Require user to be authenticated - raises exception if not."""
#     user = request.session.get("user")
#     if user and user["status"] != UserStatusEnum.active:
#         raise air.HTTPException(
#             status_code=status.HTTP_303_SEE_OTHER, headers={"HX-Redirect": "/activate", "Location": "/activate"}
#         )
#     if not user:
#         # For HTMX requests, return 401 to trigger redirect
#         if request.headers.get("HX-Request"):
#             raise air.HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, headers={"HX-Redirect": "/login"}
#             )
#         # For regular requests, redirect to login
#         raise air.HTTPException(
#             status_code=status.HTTP_303_SEE_OTHER, headers={"HX-Redirect": "/login", "Location": "/login"}
#         )
#     return user


# require_auth_dependency = Depends(require_auth)


# def _encrypt_activate_token(email: str) -> str:
#     """
#     Encrypts a JSON object containing the email and the current UTC timestamp.
#     Returns the encrypted string.
#     """
#     payload = {"email": email, "timestamp": datetime.now(timezone.utc).isoformat()}
#     payload_bytes = json.dumps(payload).encode("utf-8")
#     encrypted = fernet.encrypt(payload_bytes)
#     return encrypted.decode("utf-8")


# def _decrypt_activate_token(token: str, duration_in_seconds: int) -> dict:
#     """
#     Decrypts the encrypted string created by encrypt_email.

#     Returns a dict with:
#         - email (str)
#         - active (bool) -> True if not yet expired
#     """
#     try:
#         decrypted_bytes = fernet.decrypt(token.encode("utf-8"))
#         payload = json.loads(decrypted_bytes.decode("utf-8"))
#     except InvalidToken:
#         timestamp = datetime.now(timezone.utc) - timedelta(seconds=-5)
#         payload = {'email': '', 'timestamp': timestamp.isoformat()}

#     email = payload["email"]
#     timestamp = datetime.fromisoformat(payload["timestamp"])

#     active = datetime.now(timezone.utc) < (
#         timestamp + timedelta(seconds=duration_in_seconds)
#     )

#     return {"email": email, "active": active}


# def post_email(
#     to: str, subject: str, text: str, html: str, mailserver: str = "mailhog"
# ) -> dict:
#     data = {
#         "from": "hi@feldroy.com",
#         "to": to,
#         "subject": subject,
#         "text": text,
#         "html": html
#     }
#     req = email_client.messages.create(data=data, domain="mg.feldroy.com")
#     return req


# ### ROUTERS

# router = air.AirRouter()


# class CheckEmailForm(pydantic.BaseModel):
#     email: pydantic.EmailStr


# @router.page
# async def start(msg: str = ""):
#     if msg:
#         msg = air.Article(air.Aside(air.P(msg)))
#     return air.layouts.mvpcss(
#         air.H1("Signup form"),
#         air.Form(
#             msg,
#             air.Label("Email", for_="email"),
#             air.Input(name="email", type="email", id="email", required=True, autofocus=True),
#             air.Label("Password", for_="password", required=True),
#             air.Input(name="password", type="password", id="password"),
#             air.Button("Signup"),
#             air.P(air.Small('or ', air.A('login', href='/login'))),
#             method="post",
#             action="/signup",
#         ),
#     )


# @router.post("/start")
# async def start_form(request: air.Request, msg: str = ""):
#     form = await request.form()
#     try:
#         email = CheckEmailForm(email=form.get("email")).email
#     except pydantic.ValidationError:
#         email = ""
#     if msg:
#         msg = air.Article(air.Aside(air.P(msg)))
#     return air.layouts.mvpcss(
#         air.H1("Signup form"),
#         air.Form(
#             msg,
#             air.Label("Email", for_="email"),
#             air.Input(
#                 name="email", type="email", value=email, id="email", required=True,
#                 autofocus=True
#             ),
#             air.Label("Password", for_="password", required=True),
#             air.Input(name="password", type="password", id="password"),
#             air.Button("Signup"),
#             air.P(air.Small('or ', air.A('login', href='/login'))),
#             method="post",
#             action="/signup",
#         ),
#     )


# class UserPasswordForm(pydantic.BaseModel):
#     email: pydantic.EmailStr
#     password: str  # We use str here because we're going to save it to the database


# def _email_activatation(email: str):
#     token = _encrypt_activate_token(email=email)
#     html = air.Tags(
#                    air.H1('Activation'),
#                    air.P('Activate your account with a simple click'),
#                    air.P(air.A('Activate your account', href=f'{DOMAIN}/activate/{token}')),
#                    air.P(f"If that link doesn't work, copy/paste this into your browser: {DOMAIN}/activate/{token}")
#                ).render()
#     post_email(to=email,subject='Activate your account',
#                text='Go look at the HTML',
#                html=html
#     )

# @router.post("/signup")
# async def signup(
#     request: air.Request,background_tasks: air.BackgroundTasks, dbsession: air.db.sql.AsyncSession = async_dbsession_dependency,

# ):
#     form = await request.form()
#     email, password = form.get("email"), form.get("password")
#     try:
#         signup = UserPasswordForm(email=email, password=password)
#     except pydantic.ValidationError:
#         msg = "Try again TODO add more specific error"
#         return air.RedirectResponse(f"/start?email={email}&msg={html.escape(msg)}")
#     if len(signup.password.strip()) < 6:
#         msg = "Password not long enough"
#         return air.RedirectResponse(f"/start?email={email}&msg={html.escape(msg)}")

#     statement = select(User).where(User.email == email)
#     result = await dbsession.exec(statement)
#     user = result.first()
#     if user is None:
#         # signup - add account
#         user = User.create_user(
#             email=email,
#             password=password
#         )
#         dbsession.add(user)
#         user = await dbsession.commit()
#         background_tasks.add_task(_email_activatation, email)
#         return air.RedirectResponse("/activate", status_code=303)

#     background_tasks.add_task(_email_activatation, email)
#     return air.RedirectResponse("/activate", status_code=303)


# @router.page
# def activate():
#     return air.layouts.mvpcss(
#         air.H1("Activate account"),
#         air.P("Please check your email to activate your account."),
#         air.P("If you did not receive an email, please contact support."),
#         air.P("You can also ", air.A('login', href='/login'), " or ", air.A('sign up', href='/start'))
#     )


# @router.get("/activate/{token}")
# async def activate(
#     token: str = "", dbsession: AsyncSession = async_dbsession_dependency
# ):
#     if not token:
#         return air.layouts.mvpcss(air.H1("Activate"), air.P("This is not a valid token"))

#     data = _decrypt_activate_token(token, duration_in_seconds=600)
#     if data['active'] is False:
#         msg = "Activation code has timed out. You need to start over."
#         return air.RedirectResponse(f"/start?msg={html.escape(msg)}")

#     statement = select(User).where(User.email == data['email'])
#     result = await dbsession.exec(statement)
#     user = result.first()
#     if user is None:
#         # tell user this is bogus
#         msg = "That did not work, start over."
#         return air.RedirectResponse(f"/start?msg={html.escape(msg)}")
#     else:
#         # activate the user then tell them to log in
#         user.status = UserStatusEnum.active
#         dbsession.add(user)
#         await dbsession.commit()
#         msg = "Account activated. Go login!"
#         return air.RedirectResponse(f"/login?msg={html.escape(msg)}")


# @router.page
# def login(msg: str = ""):
#     if msg:
#         msg = air.Article(air.Aside(air.P(msg)))
#     return air.layouts.mvpcss(
#         air.H1("Login"),
#         air.Form(
#             msg,
#             air.Label("Email", for_="email"),
#             air.Input(name="email", type="email", id="email", required=True, autofocus=True),
#             air.Label("Password", for_="password", required=True),
#             air.Input(name="password", type="password", id="password"),
#             air.Button("Login"),
#             air.P(air.Small('or ', air.A('sign up', href='/start'))),
#             method="post",
#             action="/login",
#         ),
#     )


# @router.post("/login")
# async def login_action(
#     request: air.Request, dbsession: AsyncSession = async_dbsession_dependency
# ):
#     form = await request.form()
#     email, password = form.get("email"), form.get("password")
#     try:
#         UserPasswordForm(email=email, password=password)
#     except pydantic.ValidationError:
#         msg = "Try again TODO add more specific error"
#         return air.RedirectResponse(f"/login?email={email}&msg={html.escape(msg)}")

#     password_hash = hashlib.sha256(
#                 password.encode()
#             ).hexdigest()

#     statement = (
#         select(User).where(User.email == email).where(User.password_hash == password_hash)
#     )
#     result = await dbsession.exec(statement)
#     user = result.first()
#     if user is None:
#         # Redirect user back to login form
#         msg = "Username or password is incorrect"
#         return air.RedirectResponse(f"/login?msg={html.escape(msg)}", status_code=303)
#     request.session["user"] = dict(id=user.id, email=user.email, status=user.status)
#     return air.RedirectResponse("/dashboard", status_code=303)


# @router.post("/logout")
# async def logout(request: air.Request):
#     request.session.clear()
#     raise air.HTTPException(
#             status_code=status.HTTP_303_SEE_OTHER, headers={"HX-Redirect": "/login"}
#         )
