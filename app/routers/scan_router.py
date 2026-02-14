from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.guest_model import Guest
from app.models.attendance_model import AttendanceLog
from app.dependencies import get_current_admin
from app.services.qr_service import QRService

router = APIRouter(prefix="/scan", tags=["QR Scan"])

@router.post("/")
def scan_qr(token: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    guest = db.query(Guest).filter(Guest.unique_token == token).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    # Check duplicate scan
    existing = db.query(AttendanceLog).filter(AttendanceLog.guest_id == guest.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Guest already scanned")

    # Validate QR code
    if not QRService.validate_qr(guest.invitation, token):
        raise HTTPException(status_code=400, detail="Invalid QR")

    # Record attendance
    log = AttendanceLog(guest_id=guest.id)
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"status": "success", "guest": guest.name}
