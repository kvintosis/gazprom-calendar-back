from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    type: str
