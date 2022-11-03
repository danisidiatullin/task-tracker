import datetime
import enum
from typing import List, Optional

from pydantic import EmailStr, validator
from sqlmodel import Field, Relationship, SQLModel


class Role(enum.Enum):
    manager = "manager"
    developer = "developer"


class UserBase(SQLModel):
    username: str = Field(index=True, max_length=100)
    password: str = Field(max_length=256, min_length=6)
    email: EmailStr
    role: Role
    photo: Optional[str] = None
    created_at: datetime.datetime = datetime.datetime.now()


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v


class UserRead(UserBase):
    id: int
    tasks: List["TaskRead"] = []


class UserLogin(SQLModel):
    username: str
    password: str


class ChangePassword(SQLModel):
    old_password: str
    new_password: str
    new_password2: str

    @validator("new_password2")
    def password_match(cls, v, values, **kwargs):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("passwords don't match")
        return v


class UserRoleUpdate(SQLModel):
    role: Role
