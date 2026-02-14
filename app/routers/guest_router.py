from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import csv, io
import uuid
from app.models.guest_model import Guest
from app.schemas.guest_schema import GuestCreate, GuestOut
from app.database import get_db
from app.dependencies import get_current_admin
from app.services.invitation_service import InvitationService

router = APIRouter(prefix="/guests", tags=["Guests"])

@router.post("/", response_model=GuestOut)
def add_guest(guest_in: GuestCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    unique_token = str(uuid.uuid4())
    guest = Guest(**guest_in.dict(), unique_token=unique_token)
    db.add(guest)
    db.commit()
    db.refresh(guest)
    InvitationService.create_invitation(db, guest)
    return guest

@router.post("/upload-csv")
def upload_guests(file: UploadFile = File(...), event_id: int = None, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    added_guests = []

    for row in reader:
        unique_token = str(uuid.uuid4())
        guest = Guest(
            event_id=event_id,
            name=row.get("name"),
            email=row.get("email"),
            phone=row.get("phone"),
            category=row.get("category") or "NORMAL",
            unique_token=unique_token
        )
        db.add(guest)
        db.commit()
        db.refresh(guest)
        InvitationService.create_invitation(db, guest)
        added_guests.append(guest.name)
    return {"added": added_guests}
