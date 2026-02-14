from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id", ondelete="CASCADE"), nullable=False, unique=True)
    card_link = Column(String(255), nullable=False)
    qr_code_path = Column(String(255), nullable=False)
    sent_status = Column(Boolean, default=False)
    sent_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    guest = relationship("Guest", backref="invitation", passive_deletes=True)
