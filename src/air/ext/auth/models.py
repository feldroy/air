"""TODO: Move this to air.ext.user"""

from enum import StrEnum

from sqlmodel import Field, SQLModel


class UserStatusEnum(StrEnum):
    """Status for users, more will be added as needed.

    ARGS:
        unconfirmed: User has been created but hasn't yet proven they actually exist.
        active: User has proven their existence
        suspended: User's account is on hold.
    """

    unconfirmed = "Unconfirmed"
    active = "Active"
    suspended = "Suspended"


class BaseUser(SQLModel):
    """Base model for users in Air. Currently only supports GitHub OAuth.

    ARGS:

        id: Primary key for the User table.
        status: Connected to `UserStatusEnum`.
        github_oauth_access_token: Field for storing GitHub token set for user

    Example:

        import air
        from sqlmodel import Field
        from datetime import datetime

        class User(air.ext.auth.BaseUser, table=True):
            __table__ = 'auth_user'
            created_at: datetime = datetime.now()
            updated_at: datetime = datetime.now()

    """

    id: int | None = Field(default=None, primary_key=True)
    status: UserStatusEnum = UserStatusEnum.unconfirmed
    github_oauth_access_token: str | None = Field(default=True, index=True)
