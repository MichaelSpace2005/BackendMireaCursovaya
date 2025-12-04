from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repos.mechanic_repo import IMechanicRepository
from app.entities.mechanic import GameMechanic
from app.infra.database.models import MechanicDB

class MechanicRepository(IMechanicRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, mechanic: GameMechanic) -> GameMechanic:
        db = MechanicDB(name=mechanic.name, description=mechanic.description, year=mechanic.year)
        self.session.add(db)
        await self.session.commit()
        await self.session.refresh(db)
        return GameMechanic(id=db.id, name=db.name, description=db.description, year=db.year)

    async def get_by_id(self, id: int) -> Optional[GameMechanic]:
        result = await self.session.get(MechanicDB, id)
        if not result:
            return None
        return GameMechanic(id=result.id, name=result.name, description=result.description, year=result.year)

    async def list_all(self) -> List[GameMechanic]:
        q = await self.session.execute(select(MechanicDB))
        rows = q.scalars().all()
        return [GameMechanic(id=r.id, name=r.name, description=r.description, year=r.year) for r in rows]