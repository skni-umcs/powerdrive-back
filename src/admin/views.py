from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_db
from src.user.schemas import User
from src.admin.service import add_admin, delete_admin, get_all_admins
from src.admin.exceptions import UserNotFoundException

api_router = APIRouter(prefix="/admin", tags=["admin"])


@api_router.post("/{user_id}", response_model=User)
async def add(user_id: int, db: Session = Depends(get_db)):
    try:
        user = add_admin(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return user


@api_router.delete("/{user_id}", status_code=204)
async def delete(user_id: int, db: Session = Depends(get_db)):
    try:
        user = delete_admin(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@api_router.get("/", response_model=list[User])
async def get_all(db: Session = Depends(get_db)):
    return get_all_admins(db)



