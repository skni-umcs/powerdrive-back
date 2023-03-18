from sqlalchemy.orm import Session

from sqlalchemy import or_

from .schemas import CalendarCreate, CalendarUpdate, EventCreate, EventUpdate, ReoccurrenceCreate, ReoccurrenceUpdate, CycleCreate, CycleUpdate, EventCycleCreate, EventCycleUpdate, ReoccurrenceCycleCreate, ReoccurrenceCycleUpdate
from .models import Calendar, Event, Reoccurrence, Cycle, EventCycle, ReoccurrenceCycle


def get_calendar(db: Session, calendar_id: int):
    return db.query(Calendar).filter(Calendar.id == calendar_id).first()


def get_user_calendars(db: Session, user_id: int):
    return db.query(Calendar).filter(Calendar.user_id == user_id).all()


def create_calendar(db: Session, calendar: CalendarCreate, user_id: int):
    db_calendar = Calendar(**calendar.dict())
    db_calendar.user_id = user_id
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


def get_reoccurrence(db: Session, reoccurrence_id: int):
    return db.query(Reoccurrence).filter(Reoccurrence.id == reoccurrence_id).first()


def get_reoccurrences(db: Session, calendar_id: int):
    return db.query(Reoccurrence).filter(Reoccurrence.calendar_id == calendar_id).all()


def get_reoccurrences_date_constrained(db: Session, calendar_id: int, start_date: str, end_date: str):
    return db.query(Reoccurrence).filter(Reoccurrence.calendar_id == calendar_id)\
        .filter(or_(Reoccurrence.start_date <= end_date, Reoccurrence.end_date >= start_date)).all()

