from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.user.service import get_by_username
from .exceptions import InvalidCredentialsException
from .models import LoginResponse
from .security import authenticate_user, create_access_token_for_user, create_refresh_token_for_user, get_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, oauth2_scheme

api_router = APIRouter(prefix="/auth", tags=["auth"])


@api_router.post("/login", tags=["login"], response_model=LoginResponse)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(login_data.username, login_data.password, db)
    if not user:
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token_for_user(user, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token_for_user(user, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type": "bearer",
    }


@api_router.post("/refresh", tags=["refresh"], response_model=LoginResponse)
def refresh(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = get_token(token)
    if token_data.type != "refresh":
        raise InvalidCredentialsException()

    user = get_by_username(db, token_data.username)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token_for_user(user, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token_for_user(user, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type": "bearer",
    }
