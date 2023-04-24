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
    __tablename__ = 'pd_calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)

    block_color = Column(String(7), nullable=False, default='#000000')

    owner_id = Column(Integer, ForeignKey('pd_user.id'), nullable=False)
    default = Column(Boolean, nullable=False, default=False)


class Event(Base):
    __tablename__ = 'pd_event'

    id = Column(Integer, eventIDSeq, primary_key=True)
    name = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)

    block_color = Column(String(7), nullable=False, default='#000000')

    organizer_id = Column(Integer, ForeignKey('pd_user.id'), nullable=False)
    calendar_id = Column(Integer, ForeignKey('pd_calendar.id'), nullable=False)


class ReoccurringEvent(Base):
    __tablename__ = 'pd_reoccurring_event'

    id = Column(Integer, eventIDSeq, primary_key=True)
    name = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    block_color = Column(String(7), nullable=False, default='#000000')

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

    organizer_id = Column(Integer, ForeignKey('pd_user.id'), nullable=False)
    calendar_id = Column(Integer, ForeignKey('pd_calendar.id'), nullable=False)
