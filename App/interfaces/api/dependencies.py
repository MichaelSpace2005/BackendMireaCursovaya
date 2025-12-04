from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status, Header

from app.infra.database.session import AsyncSessionLocal
from app.infra.repos_impl.mechanic_repo_impl import MechanicRepository
from app.infra.repos_impl.link_repo_impl import LinkRepository
from app.infra.repos_impl.user_repo_impl import UserRepository, EmailTokenRepository
from app.infra.security import verify_access_token

async def get_db_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session

# Factories for repo instances
def get_mechanic_repo(session):
    return MechanicRepository(session)

def get_link_repo(session):
    return LinkRepository(session)

def get_user_repo(session):
    return UserRepository(session)

def get_email_token_repo(session):
    return EmailTokenRepository(session)

# Get current user from JWT token
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    
    email = verify_access_token(token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return email
