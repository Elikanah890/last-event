from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class EventStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    closed = "closed"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    banner_image = Column(String(255), nullable=True)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.draft, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
