from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.event_model import Event
from app.schemas.event_schema import EventCreate, EventOut, EventUpdate
from app.database import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/events", tags=["Events"])

# -----------------------------
# Create Event
# -----------------------------
@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    event = Event(**event_in.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# -----------------------------
# List All Events
# -----------------------------
@router.get("/", response_model=List[EventOut])
def list_events(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    events = db.query(Event).order_by(Event.start_time.desc()).all()
    return events

# -----------------------------
# Update Event
# -----------------------------
@router.put("/{event_id}", response_model=EventOut)
def update_event(
    event_id: int,
    event_in: EventUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event_in.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event
