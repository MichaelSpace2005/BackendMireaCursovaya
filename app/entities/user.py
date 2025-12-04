from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    is_verified: bool = False
    created_at: Optional[datetime] = None

@dataclass
class EmailToken:
    id: Optional[int]
    user_id: int
    token: str
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_used: bool = False
