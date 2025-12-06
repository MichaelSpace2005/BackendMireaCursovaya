from abc import ABC, abstractmethod
from typing import Optional

from app.entities.user import User


class IUserRepository(ABC):
    """Interface for user repository"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create new user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[User]:
        """Get user by id"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user"""
        pass
