from sqlalchemy.orm import Session

from sqlalchemy import or_

from .schemas import CalendarCreate, CalendarUpdate, EventCreate, EventUpdate, ReoccurringEventCreate, ReoccurringEventUpdate, EventsCycleCreate, EventsCycleUpdate, EventToCycleCreate, EventToCycleUpdate, ReoccurringEventToCycleCreate, ReoccurringEventToCycleUpdate
from .models import Calendar, Event, ReoccurringEvent, EventsCycle, EventToCycle, ReoccurringEventToCycle
from .exceptions import CalendarNameTakenException


def get_calendar(db: Session, calendar_id: int):
    return db.query(Calendar).filter(Calendar.id == calendar_id).first()


def get_user_calendars(db: Session, user_id: int):
    return db.query(Calendar).filter(Calendar.owner_id == user_id).all()


def create_calendar(db: Session, calendar: CalendarCreate, user_id: int) -> Calendar:
    existing = db.query(Calendar).filter(Calendar.owner_id == user_id).filter(Calendar.name == calendar.name).first()
    if existing:
        raise CalendarNameTakenException()
    db_calendar = Calendar(**calendar.dict())
    db_calendar.owner_id = user_id
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def update_calendar(db: Session, calendar: CalendarUpdate):
    db_calendar = db.query(Calendar).filter(Calendar.id == calendar.id).first()
    db_calendar.name = calendar.name
    db_calendar.description = calendar.description
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def delete_calendar(db: Session, calendar_id: int):
    db_calendar = db.query(Calendar).filter(Calendar.id == calendar_id).first()
    db.delete(db_calendar)
    db.commit()


def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, calendar_id: int):
    return db.query(Event).filter(Event.calendar_id == calendar_id).all()


def get_events_date_constrained(db: Session, calendar_id: int, start_date: str, end_date: str):
    return db.query(Event).filter(Event.calendar_id == calendar_id)\
        .filter(or_(Event.start_date <= end_date, Event.end_date >= start_date)).all()


def create_event(db: Session, event: EventCreate, user_id: int):
    db_event = Event(**event.dict())
    db_event.calendar_id = user_id
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_reoccurrence(db: Session, reoccurringEvent_id: int):
    return db.query(ReoccurringEvent).filter(ReoccurringEvent.id == reoccurringEvent_id).first()


def get_reoccurrences(db: Session, calendar_id: int):
    return db.query(ReoccurringEvent).filter(ReoccurringEvent.calendar_id == calendar_id).all()


def get_reoccurrences_date_constrained(db: Session, calendar_id: int, start_date: str, end_date: str):
    return db.query(ReoccurringEvent).filter(ReoccurringEvent.calendar_id == calendar_id)\
        .filter(or_(ReoccurringEvent.start_date <= end_date, ReoccurringEvent.end_date >= start_date)).all()

