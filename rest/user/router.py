from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.connectors import userConnector
from database.exceptions.userExceptions import UserNotFoundException, UsernameTakenException, IndexTakenException

from fastapi import APIRouter, Depends, HTTPException, status

from rest.user.schemas import User, UserCreate, UserUpdate
from .security_utils import get_current_user, Token, TokenData, authenticate_user, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_db

api_router = APIRouter(prefix="/user", tags=["user"])


@api_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@api_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = userConnector.get_user_by_index(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.get("/", response_model=list[User])
async def get_all_users(db: Session = Depends(get_db)):
    return userConnector.get_all_users(db)


@api_router.post("/", response_model=User)
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = userConnector.add_user(db, user.username, user.first_name, user.last_name,
                                              user.password)
    except (UsernameTakenException, IndexTakenException) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return created_user


@api_router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        userConnector.update_user_by_index(db, user_id, user.username, user.umcs_index, user.first_name, user.last_name,
                                           user.password)
    except (UserNotFoundException, UsernameTakenException, IndexTakenException) as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        userConnector.delete_user_by_index(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
