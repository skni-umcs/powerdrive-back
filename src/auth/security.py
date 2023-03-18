from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .models import TokenData
from .exceptions import InvalidCredentialsException, InactiveUserException

from src.user.service import get_by_username
from src.user.exceptions import UserNotFoundException
from src.user.models import User
from src.user.models import verify_password

from src.dependencies import get_db
from sqlalchemy.orm import Session

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# TODO probably should be taken from env variable (generated by: openssl rand -hex 32)
SECRET_KEY = "de50745a703fbb62285736c1038ac45434f8ec90f20233c2586c22590e628d15"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    try:
        user = get_by_username(db, username)
    except UserNotFoundException:
        return None

    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None or token_type not in ("access", "refresh"):
            raise InvalidCredentialsException(headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(username=username, type=token_type)
    except JWTError:
        raise InvalidCredentialsException(headers={"WWW-Authenticate": "Bearer"})
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User | None:
    exc = InvalidCredentialsException(headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None:
            raise exc
        token_data = TokenData(username=username, type=token_type)
    except JWTError:
        raise exc
    user = get_by_username(db, username=token_data.username)
    if user is None:
        raise exc
    return user


async def get_token_str(token: str = Depends(oauth2_scheme)):
    return token


async def get_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise InactiveUserException()
    return current_user


def create_access_token_for_user(user: User, expires_delta: timedelta | None = None) -> str:
    return create_access_token(data={"sub": user.username}, expires_delta=expires_delta)


def create_refresh_token_for_user(user: User, expires_delta: timedelta | None = None) -> str:
    return create_refresh_token(data={"sub": user.username}, expires_delta=expires_delta)
