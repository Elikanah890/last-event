from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EventStatus(str, Enum):
    draft = "draft"
    active = "active"
    closed = "closed"

# -----------------------------
# Input Schemas
# -----------------------------
class EventCreate(BaseModel):
    name: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    description: str | None = None
    start_time: datetime
    end_time: datetime
    status: EventStatus = EventStatus.draft

class EventUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: EventStatus | None = None

# -----------------------------
# Output Schemas
# -----------------------------
class EventOut(BaseModel):
    id: int
    name: str
    location: str
    description: str | None
    banner_image: str | None
    start_time: datetime
    end_time: datetime
    status: EventStatus
    created_at: datetime

    class Config:
        from_attributes = True
