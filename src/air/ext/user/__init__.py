"""
Implementing the User model with GitHub OAuth.

!!! note "Coming Soon: More authentication types!"

    We chose GitHub OAuth because configuring it is straightforward. Our plan is to expand to other OAuth providers as well as other registration and authentication mechanisms.

# Setup

## Step 1: Configuration

First, set these two environment variables based on your GitHub app configuration:

- GITHUB_CLIENT_ID
- GITHUB_CLIENT_SECRET

## Step 2: Add model for persistence

```python
import air
from sqlmodel import SQLModel

class User(air.ext.user.BaseUser):
    __table__ = 'user_user'
    
# TODO add tooling for generating table without Alembic
```

## Step 3: Bring in routes

```python
import air

app = air.Air()
app.add_middleware(air.SessionMiddleware, secret_key="change-me")
app.include_router(air.ext.user.user_router, prefix='/account')
```

Try it out!

---

# API

"""

from ..user.router import (
    GITHUB_CLIENT_ID as GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET as GITHUB_CLIENT_SECRET,
    user_router as user_router,
    github_login as github_login,
    github_callback as github_callback,
)
from ..user.models import (
    BaseUser as BaseUser,
    UserStatusEnum as UserStatusEnum
)
