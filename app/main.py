from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import get_settings
from app.routers import (
    auth_router,
    event_router,
    guest_router,
    invitation_router,
    scan_router,
)
from app.utils.logger import get_logger
from fastapi.openapi.utils import get_openapi
from fastapi import HTTPException, status

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

# Security scheme for Swagger (HTTP Bearer)
bearer_scheme = HTTPBearer()

# Dependency to use JWT in your routers
def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    # Optionally, you can verify token here using your SECRET_KEY
    return token

# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(event_router.router, prefix="/events", tags=["Events"])
app.include_router(guest_router.router, prefix="/guests", tags=["Guests"])
app.include_router(invitation_router.router, prefix="/invitations", tags=["Invitations"])
app.include_router(scan_router.router, prefix="/scan", tags=["QR Scan"])

# Customize OpenAPI to use Bearer token in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply globally to all endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Startup event
@app.on_event("startup")
def on_startup():
    logger.info("✅ Event Management Backend started successfully.")

# Shutdown event
@app.on_event("shutdown")
def on_shutdown():
    logger.info("⚠️ Event Management Backend shutting down.")
