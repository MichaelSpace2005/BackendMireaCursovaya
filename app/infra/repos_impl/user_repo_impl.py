from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repos.user_repo import IUserRepository, IEmailTokenRepository
from app.entities.user import User, EmailToken
from app.infra.database.models import UserDB, EmailTokenDB

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        db = UserDB(
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            is_verified=user.is_verified
        )
        self.session.add(db)
        await self.session.commit()
        await self.session.refresh(db)
        return User(
            id=db.id,
            email=db.email,
            username=db.username,
            hashed_password=db.hashed_password,
            is_verified=db.is_verified,
            created_at=db.created_at
        )

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(UserDB).where(UserDB.email == email))
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
        result = await self.session.execute(select(UserDB).where(UserDB.username == username))
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
        result = await self.session.get(UserDB, id)
        if not result:
            return None
        return User(
            id=result.id,
            email=result.email,
            username=result.username,
            hashed_password=result.hashed_password,
            is_verified=result.is_verified,
            created_at=result.created_at
        )

    async def update(self, user: User) -> User:
        result = await self.session.get(UserDB, user.id)
        if result:
            result.email = user.email
            result.username = user.username
            result.hashed_password = user.hashed_password
            result.is_verified = user.is_verified
            await self.session.commit()
            await self.session.refresh(result)
            return User(
                id=result.id,
                email=result.email,
                username=result.username,
                hashed_password=result.hashed_password,
                is_verified=result.is_verified,
                created_at=result.created_at
            )
        raise ValueError(f"User {user.id} not found")

class EmailTokenRepository(IEmailTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, token: EmailToken) -> EmailToken:
        db = EmailTokenDB(
            user_id=token.user_id,
            token=token.token,
            expires_at=token.expires_at,
            is_used=token.is_used
        )
        self.session.add(db)
        await self.session.commit()
        await self.session.refresh(db)
        return EmailToken(
            id=db.id,
            user_id=db.user_id,
            token=db.token,
            created_at=db.created_at,
            expires_at=db.expires_at,
            is_used=db.is_used
        )

    async def get_by_token(self, token: str) -> Optional[EmailToken]:
        result = await self.session.execute(select(EmailTokenDB).where(EmailTokenDB.token == token))
        db_token = result.scalars().first()
        if not db_token:
            return None
        return EmailToken(
            id=db_token.id,
            user_id=db_token.user_id,
            token=db_token.token,
            created_at=db_token.created_at,
            expires_at=db_token.expires_at,
            is_used=db_token.is_used
        )

    async def mark_as_used(self, token_id: int) -> None:
        result = await self.session.get(EmailTokenDB, token_id)
        if result:
            result.is_used = True
            await self.session.commit()

    async def delete_expired(self) -> None:
        now = datetime.utcnow()
        await self.session.execute(
            select(EmailTokenDB).where(EmailTokenDB.expires_at < now)
        )
        await self.session.commit()
