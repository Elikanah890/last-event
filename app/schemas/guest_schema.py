from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class GuestCategory(str, Enum):
    VIP = "VIP"
    NORMAL = "NORMAL"

# -----------------------------
# Input Schemas
# -----------------------------
class GuestCreate(BaseModel):
    event_id: int
    name: str = Field(..., max_length=180)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=50)
    category: GuestCategory = GuestCategory.NORMAL
    profile_image: str | None = None

# For bulk CSV uploads, you can accept List[GuestCreate] in router later

# -----------------------------
# Output Schemas
# -----------------------------
class GuestOut(BaseModel):
    id: int
    event_id: int
    name: str
    email: EmailStr | None
    phone: str | None
    category: GuestCategory
    profile_image: str | None
    unique_token: str
    created_at: datetime

    class Config:
        from_attributes = True
