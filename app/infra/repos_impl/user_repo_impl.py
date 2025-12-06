from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user import User
from app.infra.database.models import UserDB
from app.interfaces.repos.user_repo import IUserRepository


class UserRepository(IUserRepository):
    """Implementation of user repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Create new user"""
        db_user = UserDB(
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            is_verified=user.is_verified
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at
        )

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        stmt = select(UserDB).where(UserDB.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at
        )

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        stmt = select(UserDB).where(UserDB.username == username)
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at
        )

    async def get_by_id(self, id: int) -> Optional[User]:
        """Get user by id"""
        db_user = await self.session.get(UserDB, id)
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at
        )

    async def update(self, user: User) -> User:
        """Update existing user"""
        db_user = await self.session.get(UserDB, user.id)
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")
        
        db_user.email = user.email
        db_user.username = user.username
        db_user.hashed_password = user.hashed_password
        db_user.is_verified = user.is_verified
        
        await self.session.commit()
        await self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at
        )
