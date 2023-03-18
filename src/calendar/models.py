from src.database.core import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Calendar(Base):
    __tablename__ = 'Calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

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


class Reoccurrence(Base):
    __tablename__ = 'Reoccurrence'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)


class Cycle(Base):
    __tablename__ = 'Cycle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    # start_date = Column(DateTime, nullable=False)
    # end_date = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=False)

    organizer_id = Column(Integer, ForeignKey('User.id'), nullable=False)


class EventCycle(Base):
    __tablename__ = 'EventCycle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('Event.id'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('Cycle.id'), nullable=False)


class ReoccurrenceCycle(Base):
    __tablename__ = 'ReoccurrenceCycle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reoccurrence_id = Column(Integer, ForeignKey('Reoccurrence.id'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('Cycle.id'), nullable=False)
