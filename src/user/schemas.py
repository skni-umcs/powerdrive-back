from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    # TODO Password with minimum 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character with custom validation
    password: str


class UserUpdate(UserBase):
    id: int
    password: str


class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True
