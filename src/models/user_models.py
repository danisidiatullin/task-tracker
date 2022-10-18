import datetime
from typing import Optional

from pydantic import EmailStr, validator
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email: EmailStr
    created_at: datetime.datetime = datetime.datetime.now()
    in_seller: bool = False


class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr
    in_seller: bool = False

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v