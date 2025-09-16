import hashlib  # TODO switch to passlib with bcrypt or better
from abc import ABC, abstractmethod
from datetime import datetime
from enum import StrEnum

import pydantic
from sqlmodel import Field, SQLModel


class BaseUser(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass


class UserStatusEnum(StrEnum):
    unconfirmed = "Unconfirmed"
    active = "Active"
    suspended = "Suspended"


class Base(SQLModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class User(Base, table=True):
    __tablename__ = "auth_user"
    id: int | None = Field(default=None, primary_key=True)
    email: pydantic.EmailStr = Field(unique=True)
    password_hash: str = Field(repr=False, default="!", exclude=True)
    status: UserStatusEnum = UserStatusEnum.unconfirmed

    @classmethod
    def create_user(cls, email: str, password: str) -> "User":
        # Hash the password before storing
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        return cls(password_hash=password_hash, email=email, status=UserStatusEnum.unconfirmed)
