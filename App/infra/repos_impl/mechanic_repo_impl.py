from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.mechanic import GameMechanic
from app.infra.database.models import MechanicDB
from app.interfaces.repos.mechanic_repo import IMechanicRepository


class MechanicRepository(IMechanicRepository):
    """Implementation of mechanic repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, mechanic: GameMechanic) -> GameMechanic:
        """Create new mechanic"""
        db_mechanic = MechanicDB(
            name=mechanic.name,
            description=mechanic.description,
            year=mechanic.year
        )
        self.session.add(db_mechanic)
        await self.session.commit()
        await self.session.refresh(db_mechanic)
        
        return GameMechanic(
            id=db_mechanic.id,
            name=db_mechanic.name,
            description=db_mechanic.description,
            year=db_mechanic.year
        )

    async def get_by_id(self, id: int) -> Optional[GameMechanic]:
        """Get mechanic by id"""
        result = await self.session.get(MechanicDB, id)
        if not result:
            return None
        
        return GameMechanic(
            id=result.id,
            name=result.name,
            description=result.description,
            year=result.year
        )

    async def list_all(self) -> List[GameMechanic]:
        """Get all mechanics"""
        stmt = select(MechanicDB)
        result = await self.session.execute(stmt)
        mechanics = result.scalars().all()
        
        return [
            GameMechanic(
                id=m.id,
                name=m.name,
                description=m.description,
                year=m.year
            )
            for m in mechanics
        ]

    async def update(self, mechanic: GameMechanic) -> GameMechanic:
        """Update existing mechanic"""
        db_mechanic = await self.session.get(MechanicDB, mechanic.id)
        if not db_mechanic:
            raise ValueError(f"Mechanic with id {mechanic.id} not found")
        
        db_mechanic.name = mechanic.name
        db_mechanic.description = mechanic.description
        db_mechanic.year = mechanic.year
        
        await self.session.commit()
        await self.session.refresh(db_mechanic)
        
        return GameMechanic(
            id=db_mechanic.id,
            name=db_mechanic.name,
            description=db_mechanic.description,
            year=db_mechanic.year
        )

    async def delete(self, id: int) -> bool:
        """Delete mechanic by id"""
        db_mechanic = await self.session.get(MechanicDB, id)
        if not db_mechanic:
            return False
        
        await self.session.delete(db_mechanic)
        await self.session.commit()
        return True
