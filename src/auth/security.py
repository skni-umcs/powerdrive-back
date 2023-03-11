from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .models import TokenData
from .exceptions import InvalidCredentialsException, InactiveUserException

from src.user.service import get_by_username
from src.user.exceptions import UserNotFoundException
from src.user.models import User
from src.user.models import verify_password, get_password_hash

from src.dependencies import get_db
from sqlalchemy.orm import Session


SECRET_KEY = "de50745a703fbb62285736c1038ac45434f8ec90f20233c2586c22590e628d15"  # openssl rand -hex 32
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")  # placeholder for a real url


def authenticate_user(username: str, password: str) -> User | None:
    try:
        db: Session = get_db()
        user = get_by_username(username)
        # user = get_user(fake_db, username)
    except UserNotFoundException:
        return None

    if not verify_password(password, user.hashed_password):
        return None
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


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User | None:
    exc = InvalidCredentialsException(headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exc
        token_data = TokenData(username=username)
    except JWTError:
        raise exc
    user = get_by_username(db, username=token_data.username)
    if user is None:
        raise exc
    return user


async def get_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise InactiveUserException()
    return current_user

