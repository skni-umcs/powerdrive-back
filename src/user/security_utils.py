from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.user import userConnector
from src.user.userExceptions import UserNotFoundException
from src.dependencies import get_db

from pydantic import BaseModel

from src.user.schemas import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094fa76ca2556c818166b7a9563b93fa099f6f0f4ca76cf63b85e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    # return plain_password == hashed_password


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    try:
        session = get_db()
        user = userConnector.get_user_by_username(session, username)
        # user = get_user(fake_db, username)
    except UserNotFoundException:
        return False

    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    username: str


