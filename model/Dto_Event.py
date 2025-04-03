from enum import Enum

from pydantic import BaseModel
from datetime import datetime
class EventType(str, Enum):
    meeting = "meeting"
    birthday = "birthday"
    other = "other"

class Dto_Event(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    type: EventType
    organizer_id: int
class EventCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    type: str
    organizer_id: int
