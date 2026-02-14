from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class EventStatus(str, Enum):
    draft = "draft"
    active = "active"
    closed = "closed"

# -----------------------------
# Input Schemas (Requests)
# -----------------------------
class EventCreate(BaseModel):
    name: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    status: EventStatus = EventStatus.draft

class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[EventStatus] = None

# -----------------------------
# Output Schema (Responses)
# -----------------------------
class EventOut(BaseModel):
    id: int
    name: str
    location: str
    description: Optional[str] = None
    banner_image: Optional[str] = None
    start_time: datetime
    end_time: datetime
    status: EventStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
