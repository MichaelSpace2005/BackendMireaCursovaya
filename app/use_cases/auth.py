from datetime import datetime, timedelta
from app.entities.user import User, EmailToken
from app.interfaces.repos.user_repo import IUserRepository, IEmailTokenRepository
from app.infra.security import hash_password, verify_password, create_access_token, generate_email_token, EMAIL_TOKEN_EXPIRE_MINUTES

class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, email_token_repo: IEmailTokenRepository):
        self.user_repo = user_repo
        self.email_token_repo = email_token_repo

    async def execute(self, email: str, username: str, password: str) -> tuple[User, EmailToken]:
        # Check if user already exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        
        existing = await self.user_repo.get_by_username(username)
        if existing:
            raise ValueError("Username already taken")
        
        # Validate input
        if not email or len(email) < 5:
            raise ValueError("Invalid email")
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        # Create user
        hashed_pwd = hash_password(password)
        new_user = User(
            id=None,
            email=email,
            username=username,
            hashed_password=hashed_pwd,
            is_verified=False
        )
        created_user = await self.user_repo.create(new_user)
        
        # Generate email verification token
        token_str = generate_email_token()
        expires_at = datetime.utcnow() + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
        email_token = EmailToken(
            id=None,
            user_id=created_user.id,
            token=token_str,
            expires_at=expires_at,
            is_used=False
        )
        created_token = await self.email_token_repo.create(email_token)
        
        return created_user, created_token

class VerifyEmailUseCase:
    def __init__(self, user_repo: IUserRepository, email_token_repo: IEmailTokenRepository):
        self.user_repo = user_repo
        self.email_token_repo = email_token_repo

    async def execute(self, token: str) -> User:
        # Get token
        email_token = await self.email_token_repo.get_by_token(token)
        if not email_token:
            raise ValueError("Invalid token")
        
        # Check if token is expired
        if datetime.utcnow() > email_token.expires_at:
            raise ValueError("Token expired")
        
        # Check if already used
        if email_token.is_used:
            raise ValueError("Token already used")
        
        # Get user and mark as verified
        user = await self.user_repo.get_by_id(email_token.user_id)
        if not user:
            raise ValueError("User not found")
        
        user.is_verified = True
        verified_user = await self.user_repo.update(user)
        
        # Mark token as used
        await self.email_token_repo.mark_as_used(email_token.id)
        
        return verified_user

class AuthenticateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, email: str, password: str) -> tuple[User, str]:
        # Get user
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        
        # Check if verified
        if not user.is_verified:
            raise ValueError("Email not verified")
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return user, access_token
