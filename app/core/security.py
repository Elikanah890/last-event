from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72  # bcrypt max password length

def hash_password(password: str) -> str:
    """
    Hash the password for storage.
    Truncate to 72 bytes to avoid bcrypt limitation.
    """
    truncated = password[:MAX_BCRYPT_BYTES]
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against the stored hash.
    Truncate to 72 bytes.
    """
    truncated = plain_password[:MAX_BCRYPT_BYTES]
    return pwd_context.verify(truncated, hashed_password)

def create_access_token(data: dict):
    """
    Generate a JWT access token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
