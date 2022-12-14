# TODO: uncomment imports and parts of schemas when constraints will start to work
from __future__ import annotations

from pydantic import BaseModel


# from rest.privilege.schemas import Privilege
# from rest.year.schemas import Year
# from rest.registration.schemas import Registration


class UserBase(BaseModel):
    id: int | None
    username: str | None
    password: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    description: str | None



class UserCreate(UserBase):
    username: str | None
    first_name: str | None
    last_name: str | None
    password: str | None

class UserUpdate(UserBase):
    id: int
    password: str


class User(UserBase):
    username: str | None
    first_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True
