from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# -----------------------------
# Input Schemas (Request)
# -----------------------------
class AdminCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)

class AdminLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

# -----------------------------
# Output Schemas (Response)
# -----------------------------
class AdminOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    profile_image: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
