from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database.session import get_session
from app.infra.repos_impl.mechanic_repo_impl import MechanicRepository
from app.infra.repos_impl.link_repo_impl import LinkRepository
from app.infra.repos_impl.user_repo_impl import UserRepository
from app.infra.security import verify_token
from app.interfaces.repos.mechanic_repo import IMechanicRepository
from app.interfaces.repos.link_repo import ILinkRepository
from app.interfaces.repos.user_repo import IUserRepository
from app.entities.user import User


async def get_db_session() -> AsyncSession:
    """Get database session"""
    async for session in get_session():
        yield session


async def get_mechanic_repository(
    session: AsyncSession = Depends(get_db_session),
) -> IMechanicRepository:
    """Get mechanic repository"""
    return MechanicRepository(session)


async def get_link_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ILinkRepository:
    """Get link repository"""
    return LinkRepository(session)


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> IUserRepository:
    """Get user repository"""
    return UserRepository(session)


async def _resolve_user(
    authorization: str,
    user_repo: IUserRepository,
    error_status: int,
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=error_status,
            detail="Missing authorization header"
        )

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=error_status,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=error_status,
            detail="Invalid authorization header"
        )

    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=error_status,
            detail="Invalid or expired token"
        )

    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=error_status,
            detail="User not found"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email not verified"
        )

    return user


async def get_current_user(
    authorization: str = Header(None),
    user_repo: IUserRepository = Depends(get_user_repository),
) -> User:
    """Get current authenticated user with 401 on missing/invalid token"""
    return await _resolve_user(authorization, user_repo, status.HTTP_401_UNAUTHORIZED)


async def get_current_user_forbidden(
    authorization: str = Header(None),
    user_repo: IUserRepository = Depends(get_user_repository),
) -> User:
    """Same as get_current_user but returns 403 when missing/invalid token"""
    return await _resolve_user(authorization, user_repo, status.HTTP_403_FORBIDDEN)
