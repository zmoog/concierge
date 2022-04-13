from datetime import datetime

from pydantic import BaseModel


class Assignment(BaseModel):
    id: str
    teacher: str
    notes: str
    starts_at: datetime
    ends_at: datetime
