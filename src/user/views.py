from sqlalchemy.orm import Session

from src.user.exceptions import UserNotFoundException, UsernameTakenException, UserEmailTakenException

from fastapi import APIRouter, Depends, HTTPException
from src.user.service import add, get_by_index, update, delete_by_index, get_all
from src.user.schemas import User, UserCreate, UserUpdate

from src.auth.security import get_current_user
from src.dependencies import get_db

api_router = APIRouter(prefix="/user", tags=["user"])


@api_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


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
    except (UsernameTakenException, UserEmailTakenException) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return created_user


@api_router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        update(db, user)
    except (UserNotFoundException, UsernameTakenException, UserEmailTakenException) as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_by_index(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
