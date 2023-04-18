import enum
from src.database.core import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Sequence


class LoopType(str, enum.Enum):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    MONTHLY_FIRST = 'MONTHLY_FIRST'
    MONTHLY_SECOND = 'MONTHLY_SECOND'
    MONTHLY_THIRD = 'MONTHLY_THIRD'
    MONTHLY_FOURTH = 'MONTHLY_FOURTH'
    MONTHLY_LAST = 'MONTHLY_LAST'
    YEARLY = 'YEARLY'
    # CUSTOM = 'custom'


eventIDSeq = Sequence('event_id_seq', start=1, increment=1, metadata=Base.metadata)


class Calendar(Base):
    __tablename__ = 'Calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)

    owner_id = Column(Integer, ForeignKey('User.id'), nullable=False)


class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, eventIDSeq, primary_key=True)
    name = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    calendar_id = Column(Integer, ForeignKey('Calendar.id'), nullable=False)


class ReoccurringEvent(Base):
    __tablename__ = 'ReoccurringEvent'

    id = Column(Integer, eventIDSeq, primary_key=True)
    name = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    loop_type = Column(Enum(LoopType), nullable=False)
    loop_period = Column(Integer, nullable=False)

    monday = Column(Boolean, nullable=True)
    tuesday = Column(Boolean, nullable=True)
    wednesday = Column(Boolean, nullable=True)
    thursday = Column(Boolean, nullable=True)
    friday = Column(Boolean, nullable=True)
    saturday = Column(Boolean, nullable=True)
    sunday = Column(Boolean, nullable=True)

    day_of_month = Column(Integer, nullable=True)
    month_of_year = Column(Integer, nullable=True)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    calendar_id = Column(Integer, ForeignKey('Calendar.id'), nullable=False)


# class EventsGroup(Base):
#     __tablename__ = 'EventsCycle'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), nullable=False)
#     # start_date = Column(DateTime, nullable=False)
#     # end_date = Column(DateTime, nullable=False)
#     description = Column(String(100), nullable=False)
#
#     organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)


# class EventToGroup(Base):
#     __tablename__ = 'EventToCycle'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     event_id = Column(Integer, ForeignKey('Event.id'), nullable=False)
#     cycle_id = Column(Integer, ForeignKey('EventsCycle.id'), nullable=False)
#
#
# class ReoccurringEventToGroup(Base):
#     __tablename__ = 'ReoccurringEventToCycle'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     reoccurrence_id = Column(Integer, ForeignKey('ReoccurringEvent.id'), nullable=False)
#     cycle_id = Column(Integer, ForeignKey('EventsCycle.id'), nullable=False)
