from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import secrets

from app.infra.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": str(user_id), "exp": expire}
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[int]:
    """Verify JWT token and extract user_id"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except jwt.PyJWTError:
        return None


def generate_email_token() -> str:
    """Generate random email verification token"""
    return secrets.token_urlsafe(32)
