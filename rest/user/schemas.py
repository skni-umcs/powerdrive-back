# TODO: uncomment imports and parts of schemas when constraints will start to work
from __future__ import annotations

from pydantic import BaseModel


# from rest.privilege.schemas import Privilege
# from rest.year.schemas import Year
# from rest.registration.schemas import Registration


class UserBase(BaseModel):
    # user_id: int | None
    username: str | None
    first_name: str | None
    last_name: str | None

    # hashed_password: str | None
    # privilege_id: int | None
    # privilege: Privilege | None
    # years: list[Year] | None
    # registrations: list[Registration] | None


class UserCreate(UserBase):
    username: str
    first_name: str
    last_name: str
    password: str
    # hashed_password: str
    # privilege_id: int
    # privilege: Privilege
    # years: list[Year]
    # registrations: list[Registration]


class UserUpdate(UserBase):
    user_id: int
    password: str | None


class User(UserBase):
    username: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
