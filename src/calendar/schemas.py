from pydantic import BaseModel


class CalendarBase(BaseModel):
    name: str
    description: str


class CalendarCreate(CalendarBase):
    pass


class CalendarUpdate(CalendarBase):
    id: int


class CalendarInDB(CalendarBase):
    id: int

    class Config:
        orm_mode = True


class Calendar(CalendarBase):
    id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    calendar_id: int


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    id: int


class EventInDB(EventBase):
    id: int

    class Config:
        orm_mode = True


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True


class ReoccurrenceBase(BaseModel):
    name: str
    start_date: str
    end_date: str
    description: str


class ReoccurrenceCreate(ReoccurrenceBase):
    pass


class ReoccurrenceUpdate(ReoccurrenceBase):
    id: int


class ReoccurrenceInDB(ReoccurrenceBase):
    id: int

    class Config:
        orm_mode = True


class Reoccurrence(ReoccurrenceBase):
    id: int

    class Config:
        orm_mode = True


class CycleBase(BaseModel):
    name: str
    description: str


class CycleCreate(CycleBase):
    pass


class CycleUpdate(CycleBase):
    id: int


class CycleInDB(CycleBase):
    id: int

    class Config:
        orm_mode = True


class Cycle(CycleBase):
    id: int

    class Config:
        orm_mode = True


class EventCycleBase(BaseModel):
    event_id: int
    cycle_id: int


class EventCycleCreate(EventCycleBase):
    pass


class EventCycleUpdate(EventCycleBase):
    id: int


class EventCycleInDB(EventCycleBase):
    id: int

    class Config:
        orm_mode = True


class EventCycle(EventCycleBase):
    id: int

    class Config:
        orm_mode = True


class ReoccurrenceCycleBase(BaseModel):
    reoccurrence_id: int
    cycle_id: int


class ReoccurrenceCycleCreate(ReoccurrenceCycleBase):
    pass


class ReoccurrenceCycleUpdate(ReoccurrenceCycleBase):
    id: int

