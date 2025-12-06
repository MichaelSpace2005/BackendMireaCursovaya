from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    username: str
    password: str


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    username: str
    is_verified: bool
    hashed_password: Optional[str] = None


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class CreateMechanicRequest(BaseModel):
    """Create mechanic request"""
    name: str
    description: Optional[str] = None
    year: Optional[int] = None


class MechanicResponse(BaseModel):
    """Mechanic response"""
    id: int
    name: str
    description: Optional[str] = None
    year: Optional[int] = None


class CreateLinkRequest(BaseModel):
    """Create link request"""
    from_id: int
    to_id: int
    type: str


class LinkResponse(BaseModel):
    """Link response"""
    id: int
    from_id: int
    to_id: int
    type: str
