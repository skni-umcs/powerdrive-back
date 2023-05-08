from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.auth.security import get_current_user
from src.user.schemas import User
from src.usersettings.schemas import UserSettings
import src.usersettings.service as service

api_router = APIRouter(prefix="/usersettings", tags=["user settings"])


@api_router.get("", response_model=UserSettings)
async def get_user_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_settings = service.get_settings_by_user_id(db, current_user.id)
    if not user_settings:
        raise HTTPException(status_code=404, detail="User settings not found")
    return user_settings


@api_router.post("", response_model=UserSettings)
async def add_user_settings(user_settings: UserSettings, current_user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    return service.add(db, user_settings, current_user.id)


@api_router.put("", response_model=UserSettings)
async def update_user_settings(user_settings: UserSettings, current_user: User = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    return service.update(db, user_settings, current_user.id)


@api_router.delete("", status_code=204)
async def delete_user_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service.delete_by_user_id(db, current_user.id)
    return None
