from datetime import datetime, timedelta

from app.entities.user import User, EmailToken
from app.entities.user import User
from app.infra.security import hash_password, verify_password, create_access_token, generate_email_token
from app.interfaces.repos.user_repo import IUserRepository


class RegisterUserUseCase:
    """Use case for user registration"""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    async def execute(self, email: str, username: str, password: str) -> User:
        """Execute user registration"""
        # Check if user exists
        existing_email = await self.user_repo.get_by_email(email)
        if existing_email:
            raise ValueError("Email already registered")
        
        existing_username = await self.user_repo.get_by_username(username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_verified=False,
            created_at=datetime.utcnow()
        )
        
        return await self.user_repo.create(user)


class AuthenticateUserUseCase:
    """Use case for user authentication"""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    async def execute(self, email: str, password: str) -> tuple[User, str]:
        """Execute user authentication and return token"""
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        if not user.is_verified:
            raise ValueError("Email not verified")
        
        token = create_access_token(user.id)
        return user, token


class VerifyEmailUseCase:
    """Use case for email verification"""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    async def execute(self, token: str) -> User:
        """Execute email verification"""
        # This would normally check email_tokens table
        # For now, simplified version
        raise NotImplementedError("Email verification requires token repository")
