from pydantic import BaseModel, validator, Field
from datetime import datetime
from .models import Event as EventModel
from .models import ReoccurringEvent as ReoccurringEventModel
import enum


WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


class LoopType(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    MONTHLY_FIRST = "MONTHLY_FIRST"
    MONTHLY_SECOND = "MONTHLY_SECOND"
    MONTHLY_THIRD = "MONTHLY_THIRD"
    MONTHLY_FOURTH = "MONTHLY_FOURTH"
    MONTHLY_LAST = "MONTHLY_LAST"
    YEARLY = "YEARLY"


def dbevent_to_schema_dict(event: EventModel | ReoccurringEventModel) -> dict:
    if isinstance(event, ReoccurringEventModel):
        return {
            "id": event.id,
            "name": event.name,
            "place": event.place,
            "start_date": event.start_date,
            "duration": event.duration,
            "description": event.description,
            "calendar_id": event.calendar_id,
            "organizer_id": event.organizer_id,
            "is_reoccurring": True,
            "loop_type": event.loop_type,
            "loop_period": event.loop_period,
            "end_date": event.end_date,
            "reoccurring_days": [day for day in WEEKDAYS if getattr(event, day)],
            "day_of_month": event.day_of_month,
            "month_of_year": event.month_of_year,
        }
    else:
        return {
            "id": event.id,
            "name": event.name,
            "place": event.place,
            "start_date": event.start_date,
            "duration": event.duration,
            "description": event.description,
            "organizer_id": event.organizer_id,
            "calendar_id": event.calendar_id,
            "is_reoccurring": False,
            "loop_type": None,
            "loop_period": None,
            "end_date": None,
            "reoccurring_days": None,
            "day_of_month": None,
            "month_of_year": None,
        }


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


# noinspection PyMethodParameters
class EventBase(BaseModel):
    name: str
    place: str
    start_date: datetime
    duration: int = Field(description="Duration in minutes", gt=0)
    description: str
    calendar_id: int
    organizer_id: int

    is_reoccurring: bool = False
    loop_type: LoopType | None = None
    loop_period: int | None = Field(None, description="Loop period in days/weeks (depending on loop type)", ge=1)
    end_date: datetime | None = None
    reoccurring_days: list[str] | None = Field(None,
                                               description="List of days of week for reoccurring event",)
    day_of_month: int | None = Field(None, description="Day of month", ge=1, le=31)
    month_of_year: int | None = Field(None, description="Month of year", ge=1, le=12)

    @validator('duration')
    def duration_validator(cls, v):
        if v < 1:
            raise ValueError('Duration must be greater than 0')
        return v

    @validator('loop_type')
    def loop_type_validator(cls, v, values):
        if values['is_reoccurring'] and v is None:
            raise ValueError('Loop type must be set if event is reoccurring')
        return v

    @validator('loop_period')
    def loop_period_validator(cls, v, values):
        if values['is_reoccurring'] and v is None:
            raise ValueError('Loop period must be set if event is reoccurring')

        if values['is_reoccurring'] and v < 1:
            raise ValueError('Loop period must be greater than 0')
        return v

    @validator('end_date')
    def end_date_validator(cls, v, values):
        if values['is_reoccurring'] and v is not None and v < values['start_date']:
            raise ValueError('End date must be greater than start date')
        return v

    @validator('reoccurring_days')
    def reoccurring_days_must_be_valid(cls, v, values):

        if values['loop_type'] == LoopType.WEEKLY and (v is None or len(v) == 0):
            raise ValueError('Reoccurring days must be set if loop type is weekly')

        if values['loop_type'] in (LoopType.MONTHLY_FIRST, LoopType.MONTHLY_SECOND, LoopType.MONTHLY_THIRD,
                                   LoopType.MONTHLY_FOURTH, LoopType.MONTHLY_LAST) and (v is None or len(v) == 0):
            raise ValueError('Reoccurring days must be set if loop type is monthly_something')
        if v is not None:
            for day in v:
                if day not in WEEKDAYS:
                    raise ValueError('Reoccurring days must be valid days of the week')
        return v

    @validator('day_of_month')
    def day_of_month_validator(cls, v, values):
        if values['loop_type'] in (LoopType.MONTHLY, LoopType.YEARLY) and v is None:
            raise ValueError('Day of month must be set if loop type is monthly or yearly')

        if values['loop_type'] == LoopType.YEARLY and values['month_of_year'] == 2 and v > 29:
            raise ValueError('Day of month must be less than 30 for monthly events in February')

        if values['loop_type'] == LoopType.YEARLY and values['month_of_year'] in (4, 6, 9, 11) and v > 30:
            raise ValueError('Day of month must be less than 31 for monthly events in April, June, September, '
                             'and November')

        return v


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    id: int


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = dbevent_to_schema_dict
