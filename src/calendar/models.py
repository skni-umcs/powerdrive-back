from src.database.core import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Calendar(Base):
    __tablename__ = 'Calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)

    owner_id = Column(Integer, ForeignKey('User.id'), nullable=False)


class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    calendar_id = Column(Integer, ForeignKey('Calendar.id'), nullable=False)


class ReoccurringEvent(Base):
    __tablename__ = 'ReoccurringEvent'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)


class EventsCycle(Base):
    __tablename__ = 'EventsCycle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    # start_date = Column(DateTime, nullable=False)
    # end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)


class EventToCycle(Base):
    __tablename__ = 'EventToCycle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('Event.id'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('EventsCycle.id'), nullable=False)


class ReoccurringEventToCycle(Base):
    __tablename__ = 'ReoccurringEventToCycle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reoccurrence_id = Column(Integer, ForeignKey('ReoccurringEvent.id'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('EventsCycle.id'), nullable=False)
