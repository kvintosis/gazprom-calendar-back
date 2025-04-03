from pydantic import BaseModel


class DTO_event(BaseModel):
    title: str
    description: str
    start_time: str
    end_time: str
    type: str
    organizer_id: str
