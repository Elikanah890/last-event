# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

# Load settings
settings = get_settings()

# Use the full DATABASE_URL from .env
DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # checks connections before using them
    pool_size=10,        # maximum number of persistent connections
    max_overflow=20,     # extra connections beyond pool_size
    echo=settings.DEBUG, # log SQL statements if DEBUG=True
)

# SessionLocal factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
Base = declarative_base()


# Dependency to get DB session in FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
