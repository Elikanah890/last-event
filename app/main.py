from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routers import (
    auth_router,
    event_router,
    guest_router,
    invitation_router,
    scan_router,
)
from app.utils.logger import get_logger

# Load settings and logger
settings = get_settings()
logger = get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Event Management Backend",
    version="1.0.0",
    description="""
Event Management Backend API

This backend allows:
- Admin authentication (register/login)
- Event CRUD operations
- Guest management and CSV upload
- Invitations listing
- QR code scanning
"""
)

# CORS settings
origins = [
    "http://localhost:5173",        # Local frontend
    settings.INVITATION_BASE_URL    # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with tags for Swagger grouping
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(event_router.router, prefix="/events", tags=["Events"])
app.include_router(guest_router.router, prefix="/guests", tags=["Guests"])
app.include_router(invitation_router.router, prefix="/invitations", tags=["Invitations"])
app.include_router(scan_router.router, prefix="/scan", tags=["QR Scan"])

# Startup event
@app.on_event("startup")
def on_startup():
    logger.info("✅ Event Management Backend started successfully.")

# Shutdown event
@app.on_event("shutdown")
def on_shutdown():
    logger.info("⚠️ Event Management Backend shutting down.")
