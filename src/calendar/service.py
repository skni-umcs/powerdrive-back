from datetime import timedelta

from sqlalchemy.orm import Session

from sqlalchemy import or_

from .schemas import CalendarCreate, CalendarUpdate, EventCreate, EventUpdate, WEEKDAYS
from .schemas import EventBase as EventBaseSchema
from .schemas import Calendar as CalendarSchema
from .models import Calendar as CalendarModel
from .models import Event as EventModel
from .models import ReoccurringEvent as ReoccurringEventModel
from .models import LoopType
from .exceptions import CalendarNameTakenException, EventAlreadyExistsException


def event_to_model(event: EventBaseSchema) -> EventModel | ReoccurringEventModel:
    try:
        event_id = event.id
    except AttributeError:
        event_id = None
    if event.is_reoccurring:
        if event.reoccurring_days is None:
            event.reoccurring_days = []
        return ReoccurringEventModel(
            id=event_id,
            name=event.name,
            place=event.place,
            start_date=event.start_date,
            duration=event.duration,
            end_date=event.end_date,
            description=event.description,
            loop_type=event.loop_type,
            loop_period=event.loop_period,
            monday=WEEKDAYS[0] in event.reoccurring_days,
            tuesday=WEEKDAYS[1] in event.reoccurring_days,
            wednesday=WEEKDAYS[2] in event.reoccurring_days,
            thursday=WEEKDAYS[3] in event.reoccurring_days,
            friday=WEEKDAYS[4] in event.reoccurring_days,
            saturday=WEEKDAYS[5] in event.reoccurring_days,
            sunday=WEEKDAYS[6] in event.reoccurring_days,
            day_of_month=event.day_of_month,
            month_of_year=event.month_of_year,
            organizer_id=event.organizer_id,
            calendar_id=event.calendar_id,
        )
    else:
        return EventModel(
            id=event_id,
            name=event.name,
            place=event.place,
            start_date=event.start_date,
            duration=event.duration,
            description=event.description,
            organizer_id=event.organizer_id,
            calendar_id=event.calendar_id,
        )


# def model_to_event(model: EventModel | ReoccurringEventModel) -> EventSchema:
#     if isinstance(model, ReoccurringEventModel):
#         return EventSchema(
#             id=model.id,
#             name=model.name,
#             place=model.place,
#             start_date=model.start_date,
#             duration=model.duration,
#             end_date=model.end_date,
#             description=model.description,
#             loop_type=model.loop_type,
#             loop_period=model.loop_period,
#             reoccurring_days=[day for day in WEEKDAYS if getattr(model, day)],
#             day_of_month=model.day_of_month,
#             month_of_year=model.month_of_year,
#             organizer_id=model.organizer_id,
#             calendar_id=model.calendar_id,
#             is_reoccurring=True,
#         )
#     else:
#         return EventSchema(
#             id=model.id,
#             name=model.name,
#             place=model.place,
#             start_date=model.start_date,
#             duration=model.duration,
#             description=model.description,
#             organizer_id=model.organizer_id,
#             calendar_id=model.calendar_id,
#             is_reoccurring=False,
#             loop_type=None,
#             loop_period=None,
#             end_date=None,
#             reoccurring_days=None,
#             day_of_month=None,
#             month_of_year=None,
#         )

def get_calendar(db: Session, calendar_id: int) -> CalendarModel:
    return db.query(CalendarModel) \
        .filter(CalendarModel.id == calendar_id) \
        .first()


def get_user_calendars(db: Session, user_id: int) -> list[CalendarModel]:
    return db.query(CalendarModel) \
        .filter(CalendarModel.owner_id == user_id) \
        .all()


def create_calendar(db: Session, calendar: CalendarCreate, user_id: int) -> CalendarModel:
    existing = db.query(CalendarModel) \
        .filter(CalendarModel.owner_id == user_id) \
        .filter(CalendarModel.name == calendar.name) \
        .first()
    if existing:
        raise CalendarNameTakenException()
    db_calendar = CalendarModel(**calendar.dict())
    db_calendar.owner_id = user_id
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def update_calendar(db: Session, calendar: CalendarUpdate):
    db_calendar = db.query(CalendarModel) \
        .filter(CalendarModel.id == calendar.id) \
        .first()
    conflicting = db.query(CalendarModel) \
        .filter(CalendarModel.owner_id == db_calendar.owner_id) \
        .filter(CalendarModel.name == calendar.name) \
        .filter(CalendarModel.id != calendar.id) \
        .first()
    if conflicting:
        raise CalendarNameTakenException()
    db_calendar.name = calendar.name
    db_calendar.description = calendar.description
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def delete_calendar(db: Session, calendar_id: int):
    delete_calendar_events(db, calendar_id)
    db_calendar = db.query(CalendarModel) \
        .filter(CalendarModel.id == calendar_id) \
        .first()
    db.delete(db_calendar)
    db.commit()


def get_event(db: Session, event_id: int):
    return db.query(EventModel).filter(EventModel.id == event_id).first() or \
        db.query(ReoccurringEventModel).filter(ReoccurringEventModel.id == event_id).first()


def get_calendar_events(db: Session, calendar_id: int):
    return db.query(EventModel).filter(EventModel.calendar_id == calendar_id).all() + \
        db.query(ReoccurringEventModel).filter(ReoccurringEventModel.calendar_id == calendar_id).all()


# def get_events(db: Session, calendar_id: int):
#     return db.query(Event).filter(Event.calendar_id == calendar_id).all()


def get_events_date_constrained(db: Session, calendar_id: int, start_date: str, end_date: str):
    return db.query(EventModel).filter(EventModel.calendar_id == calendar_id) \
        .filter(or_(EventModel.start_date <= end_date,
                    EventModel.start_date + timedelta(EventModel.duration) >= start_date)) \
        .all()


def get_user_events(db: Session, user_id: int):
    return db.query(EventModel).filter(EventModel.organizer_id == user_id).all() + \
        db.query(ReoccurringEventModel).filter(ReoccurringEventModel.organizer_id == user_id).all()


def create_event(db: Session, event: EventCreate, user_id: int):
    db_event = event_to_model(event)
    db_event.organizer_id = user_id
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event: EventUpdate):
    db_event = db.query(EventModel).filter(EventModel.id == event.id).first() or \
               db.query(ReoccurringEventModel).filter(ReoccurringEventModel.id == event.id).first()
    conflicting = db.query(EventModel) \
                      .filter(EventModel.calendar_id == event.calendar_id) \
                      .filter(EventModel.place == event.place) \
                      .filter(EventModel.name == event.name) \
                      .filter(EventModel.start_date == event.start_date) \
                      .filter(EventModel.duration == event.duration) \
                      .filter(EventModel.id != event.id).first() or \
                  db.query(ReoccurringEventModel) \
                      .filter(ReoccurringEventModel.calendar_id == event.calendar_id) \
                      .filter(ReoccurringEventModel.place == event.place) \
                      .filter(ReoccurringEventModel.name == event.name) \
                      .filter(ReoccurringEventModel.start_date == event.start_date) \
                      .filter(ReoccurringEventModel.duration == event.duration) \
                      .filter(ReoccurringEventModel.id != event.id).first()
    if conflicting:
        raise EventAlreadyExistsException()
    db_event.name = event.name
    db_event.place = event.place
    db_event.description = event.description
    db_event.start_date = event.start_date
    db_event.duration = event.duration
    db_event.calendar_id = event.calendar_id
    db.commit()

    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first() or \
               db.query(ReoccurringEventModel).filter(ReoccurringEventModel.id == event_id).first()
    db.delete(db_event)
    db.commit()


def delete_calendar_events(db: Session, calendar_id: int):
    db.query(EventModel).filter(EventModel.calendar_id == calendar_id).delete()
    db.query(ReoccurringEventModel).filter(ReoccurringEventModel.calendar_id == calendar_id).delete()
    db.commit()


def check_for_event(db: Session, event: EventCreate) -> EventModel | ReoccurringEventModel | None:
    return db.query(EventModel) \
        .filter(EventModel.calendar_id == event.calendar_id) \
        .filter(EventModel.name == event.name) \
        .filter(EventModel.place == event.place) \
        .filter(EventModel.start_date == event.start_date) \
        .filter(EventModel.duration == event.duration) \
        .first() or \
        db.query(ReoccurringEventModel) \
            .filter(ReoccurringEventModel.calendar_id == event.calendar_id) \
            .filter(ReoccurringEventModel.name == event.name) \
            .filter(ReoccurringEventModel.place == event.place) \
            .filter(ReoccurringEventModel.start_date == event.start_date) \
            .filter(ReoccurringEventModel.duration == event.duration) \
            .first()

# def get_reoccurrence(db: Session, reoccurringEvent_id: int):
#     return db.query(ReoccurringEvent).filter(ReoccurringEvent.id == reoccurringEvent_id).first()
#
#
# def get_reoccurrences(db: Session, calendar_id: int):
#     return db.query(ReoccurringEvent).filter(ReoccurringEvent.calendar_id == calendar_id).all()
#
#
# def get_reoccurrences_date_constrained(db: Session, calendar_id: int, start_date: str, end_date: str):
#     return db.query(ReoccurringEvent).filter(ReoccurringEvent.calendar_id == calendar_id) \
#         .filter(or_(ReoccurringEvent.start_date <= end_date, ReoccurringEvent.end_date >= start_date)).all()
