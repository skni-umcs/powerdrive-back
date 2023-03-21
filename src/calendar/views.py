from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from src.user.models import User

from src.calendar.schemas import Calendar, CalendarCreate, CalendarUpdate, Event, EventCreate, EventUpdate

from src.calendar.service import get_user_calendars as get_user_calendars_service
from src.calendar.service import get_calendar as get_calendar_service
from src.calendar.service import create_calendar as create_calendar_service
from src.calendar.service import update_calendar as update_calendar_service
from src.calendar.service import delete_calendar as delete_calendar_service
from src.calendar.service import get_calendar_events as get_calendar_events_service
from src.calendar.service import get_event as get_event_service
from src.calendar.service import create_event as create_event_service
from src.calendar.service import update_event as update_event_service
from src.calendar.service import delete_event as delete_event_service
from src.calendar.service import check_for_event as check_for_event_service

from src.calendar.exceptions import UnauthorizedCalendarException, EventAlreadyExistsException, UnauthorizedEventException

from src.auth.security import get_current_user
from src.dependencies import get_db


api_router = APIRouter(prefix="/calendar", tags=["calendar"])


@api_router.get("/all", response_model=list[Calendar])
async def get_calendars(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)) -> list[Calendar]:
    return get_user_calendars_service(db, current_user.id)


@api_router.post("/", response_model=Calendar)
async def create_calendar(calendar: CalendarCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Calendar:
    return create_calendar_service(db, calendar, current_user.id)


@api_router.get("/{calendar_id}", response_model=Calendar)
async def get_calendar(calendar_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_calendars = get_user_calendars_service(db, current_user.id)
    if calendar_id not in [calendar.id for calendar in user_calendars]:
        raise UnauthorizedCalendarException()

    calendar = get_calendar_service(db, calendar_id)

    return calendar


@api_router.put("/", response_model=Calendar)
async def update_calendar(calendar: CalendarUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_calendars = get_user_calendars_service(db, current_user.id)
    if calendar.id not in [calendar.id for calendar in user_calendars]:
        raise UnauthorizedCalendarException()

    db_calendar = get_calendar_service(db, calendar.id)
    if db_calendar.owner_id != current_user.id:
        raise UnauthorizedCalendarException()

    return update_calendar_service(db, calendar)


@api_router.delete("/{calendar_id}")
async def delete_calendar(calendar_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_calendars = get_user_calendars_service(db, current_user.id)
    if calendar_id not in [calendar.id for calendar in user_calendars]:
        raise UnauthorizedCalendarException()

    calendar = get_calendar_service(db, calendar_id)
    if calendar.owner_id != current_user.id:
        raise UnauthorizedCalendarException()

    delete_calendar_service(db, calendar_id)

    return {"message": "Successfully deleted calendar"}


@api_router.get("/event/all", response_model=list[Event])
async def get_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_calendars = get_user_calendars_service(db, current_user.id)
    calendar_events = []
    for calendar in user_calendars:
        calendar_events.extend(get_calendar_events_service(db, calendar.id))

    return calendar_events


@api_router.get("/{calendar_id}/event", response_model=list[Event])
async def get_events_by_calendar(calendar_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_calendars = get_user_calendars_service(db, current_user.id)
    if calendar_id not in [calendar.id for calendar in user_calendars]:
        raise UnauthorizedCalendarException()

    calendar_events = get_calendar_events_service(db, calendar_id)
    return calendar_events


@api_router.post("/{calendar_id}/event", response_model=Event)
async def create_event_in_calendar(event: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_calendars = get_user_calendars_service(db, current_user.id)
    if event.calendar_id not in [calendar.id for calendar in user_calendars]:
        raise UnauthorizedCalendarException()

    same_event = check_for_event_service(db, event)
    if same_event:
        raise EventAlreadyExistsException()

    return create_event_service(db, event, current_user.id)


@api_router.put("/event", response_model=Event)
async def update_event(event: EventUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_event = get_event_service(db, event.id)
    if not db_event:
        raise UnauthorizedEventException()

    if db_event.organizer_id != current_user.id:
        raise UnauthorizedEventException()

    return update_event_service(db, event)


@api_router.delete("/event/{event_id}")
async def delete_event(event_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    event = get_event_service(db, event_id)
    if not event:
        raise UnauthorizedEventException()

    if event.organizer_id != current_user.id:
        raise UnauthorizedEventException()

    delete_event_service(db, event_id)

    return {"message": "Successfully deleted event"}

