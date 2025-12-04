from abc import ABC, abstractmethod
from app.entities.user import User, EmailToken
from typing import List, Optional

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[User]: ...
    
    @abstractmethod
    async def update(self, user: User) -> User: ...

class IEmailTokenRepository(ABC):
    @abstractmethod
    async def create(self, token: EmailToken) -> EmailToken: ...
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[EmailToken]: ...
    
    @abstractmethod
    async def mark_as_used(self, token_id: int) -> None: ...
    
    @abstractmethod
    async def delete_expired(self) -> None: ...
