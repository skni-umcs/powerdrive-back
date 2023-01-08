from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends
from .security import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import Token
from .exceptions import InvalidCredentialsException
from src.dependencies import get_db

api_router = APIRouter(prefix="/auth", tags=["auth"])


@api_router.post("/login", tags=["login"], response_model=Token)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(login_data.username, login_data.password, db)
    if not user:
        raise InvalidCredentialsException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
