from pydantic import BaseModel, EmailStr, ValidationError, validator


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr



class UserCreate(UserBase):
    password: str
    @validator('password')
    def password_must_contain_uppercase(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @validator('password')
    def password_must_contain_lowercase(cls, v):
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

    @validator('password')
    def password_must_contain_digit(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @validator('password')
    def password_must_contain_special_character(cls, v):
        if not any(not char.isalnum() for char in v):
            raise ValueError('Password must contain at least one special character')
        return v



class UserUpdate(UserCreate):
    id: int


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
