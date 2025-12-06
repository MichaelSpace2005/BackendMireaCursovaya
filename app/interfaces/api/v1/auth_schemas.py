from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=6)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserDTO(BaseModel):
    id: int
    email: str
    username: str
    is_verified: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserDTO


class RegisterResponse(BaseModel):
    message: str
    email: str


class VerifyEmailRequest(BaseModel):
    token: str
