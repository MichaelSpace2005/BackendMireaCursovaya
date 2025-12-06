import pytest
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.infra.database.models import Base, MechanicDB, LinkDB, UserDB, EmailTokenDB
from app.infra.repos_impl.mechanic_repo_impl import MechanicRepository
from app.infra.repos_impl.link_repo_impl import LinkRepository
from app.infra.repos_impl.user_repo_impl import UserRepository
from app.entities.mechanic import GameMechanic
from app.entities.link import EvolutionLink
from app.entities.user import User


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db_session():
    """Create test database session with in-memory SQLite"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
async def mechanic_repo(test_db_session):
    """Get mechanic repository with test database"""
    return MechanicRepository(test_db_session)


@pytest.fixture
async def link_repo(test_db_session):
    """Get link repository with test database"""
    return LinkRepository(test_db_session)


@pytest.fixture
async def user_repo(test_db_session):
    """Get user repository with test database"""
    return UserRepository(test_db_session)


@pytest.fixture
async def sample_mechanic():
    """Sample mechanic for testing"""
    return GameMechanic(
        id=None,
        name="Combat System",
        description="Main combat mechanics",
        year=2024
    )


@pytest.fixture
async def sample_mechanic_2():
    """Second sample mechanic for testing"""
    return GameMechanic(
        id=None,
        name="Leveling System",
        description="Character progression mechanics",
        year=2024
    )


@pytest.fixture
async def sample_link():
    """Sample link for testing"""
    return EvolutionLink(
        id=None,
        from_id=1,
        to_id=2,
        type="inheritance"
    )


@pytest.fixture
async def sample_user():
    """Sample user for testing"""
    return User(
        id=None,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password_123",
        is_verified=True,
        created_at=datetime.utcnow()
    )


@pytest.fixture
async def created_mechanic(mechanic_repo, sample_mechanic):
    """Create and return a mechanic in database"""
    return await mechanic_repo.create(sample_mechanic)


@pytest.fixture
async def created_mechanics(mechanic_repo, sample_mechanic, sample_mechanic_2):
    """Create and return multiple mechanics"""
    mech1 = await mechanic_repo.create(sample_mechanic)
    mech2 = await mechanic_repo.create(sample_mechanic_2)
    return [mech1, mech2]


@pytest.fixture
async def created_link(link_repo, created_mechanics):
    """Create and return a link between two mechanics"""
    link = EvolutionLink(
        id=None,
        from_id=created_mechanics[0].id,
        to_id=created_mechanics[1].id,
        type="inheritance"
    )
    return await link_repo.create(link)


@pytest.fixture
async def created_user(user_repo, sample_user):
    """Create and return a user in database"""
    return await user_repo.create(sample_user)
