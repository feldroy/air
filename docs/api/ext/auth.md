# ext.auth

Implementing the User model with GitHub OAuth.

!!! note "Coming Soon: More authentication methods!"
    We chose GitHub OAuth because configuring it is straightforward. Our plan is to expand to other OAuth providers as well as other registration and authentication mechanisms.

## Step 1: Get client ID and secret

TODO: Add instructions on getting this from GitHub

!!! warning "Client secrets must be protected!"
    Do not store client secrets in your repo. This is what connects your application to GitHub, and if bad guys find it they can cause problem for you and your users. Instead, use environment variables or other proven methods for securing private credentials.


## Step 2: Write a Github Process callable to process the user when the come back from github

This is a simple in-memory version, you want to save this to a database, either SQL or non-SQL.

```python
import air

database = {}


async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
    access_token = token["access_token"]
    print(access_token)
    if access_token in database:
        database[access_token]["updated_at"] = datetime.now()
    else:
        database[access_token] = token
        database[access_token]["created_at"] = datetime.now()
        database[access_token]["updated_at"] = datetime.now()
        database[access_token]["access_token"] = access_token
    request.session["github_access_token"] = access_token
    print(database)
```

## Step 3: Use the GitHubOAuthClientFactory to generate your OAuth client

```python
github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
    github_client_id=environ["GITHUB_CLIENT_ID"],
    github_client_secret=environ["GITHUB_CLIENT_SECRET"],
    github_process_callable=github_process_callable,
    login_redirect_to="/",
)
```

## Step 4: Code up the rest of the project


```python
import air

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")
# We created github_oauth_router in step 3
app.include_router(github_oauth_client.router)


@app.page
async def index(request: air.Request):
    return air.layouts.mvpcss(
        air.H1("GitHub OAuth Login Demo"),
        air.P(air.A("Login to Github", href="/account/github/login")),
        air.P(request.session.get("github_access_token", "Not authenticated yet")),
    )
```

Try it out!

---


::: air.ext.auth
    options:
      group_by_category: false
      members:
        - GitHubOAuthClientFactory