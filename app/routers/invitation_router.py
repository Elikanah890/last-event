from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.invitation_model import Invitation
from app.database import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/invitations", tags=["Invitations"])

@router.get("/")
def list_invitations(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(Invitation).all()
