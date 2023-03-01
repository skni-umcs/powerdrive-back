from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_db
from src.user.schemas import User
from src.admin.service import add_admin, delete_admin, get_all_admins
from src.admin.exceptions import UserNotAdminException
from src.auth.security import get_current_user
api_router = APIRouter(prefix="/admin", tags=["admin"])


def is_current_admin(user: User = Depends(get_current_user)):
    if user.if_admin:
        return user
    else:
        raise HTTPException(status_code=404, detail=str(UserNotAdminException))


@api_router.post("/{user_id}", response_model=User)
async def add(user_id: int, db: Session = Depends(get_db), admin: User = Depends(is_current_admin)):
    try:
        user = add_admin(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.delete("/{user_id}", status_code=204)
async def delete(user_id: int, db: Session = Depends(get_db), admin: User = Depends(is_current_admin)):
    try:
        user = delete_admin(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@api_router.get("/", response_model=list[User])
async def get_all(db: Session = Depends(get_db), admin: User = Depends(is_current_admin)):
    return get_all_admins(db)



