from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from app.infra.database.models import Base
from app.infra.config import settings

# Create engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)

async def init_models(engine):
    """Create all tables in database"""
    from app.infra.database import models  # Import to register models
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_engine():
    """Get the database engine"""
    return engine