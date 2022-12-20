from datetime import timedelta

# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.user.exceptions import UserNotFoundException, UsernameTakenException

from fastapi import APIRouter, Depends, HTTPException, status
from src.user.service import add, get_by_index, update, delete_by_index, get_all
from src.user.schemas import User, UserCreate, UserUpdate
# from .security_utils import Token, authenticate_user, create_access_token, \
#     ACCESS_TOKEN_EXPIRE_MINUTES
from src.dependencies import get_db

api_router = APIRouter(prefix="/user", tags=["user"])


# @api_router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @api_router.get("/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
#

@api_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_by_index(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.get("/", response_model=list[User])
async def get_all_users(db: Session = Depends(get_db)):
    return get_all(db)


@api_router.post("/", response_model=User)
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = add(db, user)
    except UsernameTakenException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return created_user


@api_router.put("/{user_id}", response_model=User, )
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        update(db, user)
    except (UserNotFoundException, UsernameTakenException) as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_by_index(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
