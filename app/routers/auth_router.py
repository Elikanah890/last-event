from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.admin_schema import AdminCreate, AdminLogin, AdminOut
from app.models.admin_model import Admin
from app.database import get_db
from app.services.token_service import TokenService
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AdminOut)
def register_admin(admin_in: AdminCreate, db: Session = Depends(get_db)):
    """
    Register a new admin.
    """
    existing = db.query(Admin).filter(Admin.email == admin_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(admin_in.password)
    admin = Admin(name=admin_in.name, email=admin_in.email, password_hash=hashed)
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@router.post("/login")
def login_admin(admin_in: AdminLogin, db: Session = Depends(get_db)):
    """
    Login admin and return access token.
    """
    admin = db.query(Admin).filter(Admin.email == admin_in.email).first()
    if not admin or not verify_password(admin_in.password, admin.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = TokenService.create_access_token({"admin_id": admin.id})
    return {"access_token": access_token, "token_type": "bearer"}
