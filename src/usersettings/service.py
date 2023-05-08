from fastapi import HTTPException

from .models import DbUserSettings
from .schemas import UserSettings
from sqlalchemy.orm import Session


def get_settings_by_user_id(db: Session, user_id: int) -> DbUserSettings:
    return db.query(DbUserSettings).filter(DbUserSettings.user_id == user_id).first()


def add(db: Session, user_settings: UserSettings, user_id: int) -> DbUserSettings:
    if get_settings_by_user_id(db, user_id):
        raise HTTPException(status_code=400, detail="User settings already exists")

    db_user_settings = DbUserSettings(**user_settings.dict(), user_id=user_id)
    db.add(db_user_settings)
    db.commit()
    db.refresh(db_user_settings)
    return db_user_settings


def update(db: Session, user_settings: UserSettings, user_id: int) -> DbUserSettings:
    db_user_settings = get_settings_by_user_id(db, user_id)
    if not db_user_settings:
        raise HTTPException(status_code=404, detail="User settings not found")
    db_user_settings.values = user_settings.values
    db.commit()
    db.refresh(db_user_settings)
    return db_user_settings


def delete_by_user_id(db: Session, user_id: int) -> None:
    db_user_settings = get_settings_by_user_id(db, user_id)
    if not db_user_settings:
        raise HTTPException(status_code=404, detail="User settings not found")
    db.delete(db_user_settings)
    db.commit()
    return None
