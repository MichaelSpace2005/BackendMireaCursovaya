from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infra.database.models import Base
from app.infra.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=20,
    max_overflow=0,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncSession:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session


async def init_models():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    """Drop all tables (for testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def get_engine():
    """Get database engine"""
    return engine


async def dispose_models():
    """Dispose engine connections"""
    await engine.dispose()
