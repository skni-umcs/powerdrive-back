from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from src.user.models import User

from src.calendar.schemas import Calendar, CalendarCreate
from src.calendar.service import get_user_calendars as get_user_calendars_service
from src.calendar.service import create_calendar as create_calendar_service

from src.auth.security import get_current_user
from src.dependencies import get_db


api_router = APIRouter(prefix="/calendar", tags=["calendar"])


@api_router.get("/")
async def get_calendars(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)) -> list[Calendar]:
    return get_user_calendars_service(db, current_user.id)


@api_router.post("/")
async def create_calendar(calendar: CalendarCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Calendar:
    return create_calendar_service(db, calendar, current_user.id)
