from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class GuestCategory(str, enum.Enum):
    VIP = "VIP"
    NORMAL = "NORMAL"

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(180), nullable=False)
    email = Column(String(180), nullable=True)
    phone = Column(String(50), nullable=True)
    category = Column(Enum(GuestCategory), default=GuestCategory.NORMAL)
    profile_image = Column(String(255), nullable=True)
    unique_token = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    event = relationship("Event", backref="guests", passive_deletes=True)
