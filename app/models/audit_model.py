from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(120), nullable=False)
    resource = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    admin = relationship("Admin", backref="audit_logs", passive_deletes=True)
