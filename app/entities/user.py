from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User domain model"""
    id: Optional[int] = None
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    is_verified: bool = False
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate user on creation"""
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.username:
            raise ValueError("Username cannot be empty")


@dataclass
class EmailToken:
    """Email verification token"""
    id: Optional[int] = None
    user_id: int = 0
    token: str = ""
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_used: bool = False
