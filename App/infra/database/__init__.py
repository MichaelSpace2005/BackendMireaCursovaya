from .models import Base, MechanicDB, LinkDB
from .engine import get_engine
from sqlalchemy.ext.asyncio import AsyncEngine

async def init_models(engine: AsyncEngine):
    # create tables if not exist (for dev). In production use alembic.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)