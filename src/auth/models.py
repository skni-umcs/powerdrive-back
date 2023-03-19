from pydantic import BaseModel


class TokenData(BaseModel):
    username: str
    type: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: str
