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


class ReoccurringEventBase(BaseModel):
    name: str
    start_date: str
    end_date: str
    description: str


class ReoccurringEventCreate(ReoccurringEventBase):
    pass


class ReoccurringEventUpdate(ReoccurringEventBase):
    id: int


class ReoccurringEventInDB(ReoccurringEventBase):
    id: int

    class Config:
        orm_mode = True


class ReoccurringEvent(ReoccurringEventBase):
    id: int

    class Config:
        orm_mode = True


class EventsCycleBase(BaseModel):
    name: str
    description: str


class EventsCycleCreate(EventsCycleBase):
    pass


class EventsCycleUpdate(EventsCycleBase):
    id: int


class EventsCycleInDB(EventsCycleBase):
    id: int

    class Config:
        orm_mode = True


class EventsCycle(EventsCycleBase):
    id: int

    class Config:
        orm_mode = True


class EventToCycleBase(BaseModel):
    event_id: int
    cycle_id: int


class EventToCycleCreate(EventToCycleBase):
    pass


class EventToCycleUpdate(EventToCycleBase):
    id: int


class EventToCycleInDB(EventToCycleBase):
    id: int

    class Config:
        orm_mode = True


class EventToCycle(EventToCycleBase):
    id: int

    class Config:
        orm_mode = True


class ReoccurringEventToCycleBase(BaseModel):
    reoccurrence_id: int
    cycle_id: int


class ReoccurringEventToCycleCreate(ReoccurringEventToCycleBase):
    pass


class ReoccurringEventToCycleUpdate(ReoccurringEventToCycleBase):
    id: int

