from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.link import EvolutionLink
from app.infra.database.models import LinkDB
from app.interfaces.repos.link_repo import ILinkRepository


class LinkRepository(ILinkRepository):
    """Implementation of link repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, link: EvolutionLink) -> EvolutionLink:
        """Create new link"""
        db_link = LinkDB(
            from_id=link.from_id,
            to_id=link.to_id,
            type=link.type
        )
        self.session.add(db_link)
        await self.session.commit()
        await self.session.refresh(db_link)
        
        return EvolutionLink(
            id=db_link.id,
            from_id=db_link.from_id,
            to_id=db_link.to_id,
            type=db_link.type
        )

    async def get_by_id(self, id: int) -> Optional[EvolutionLink]:
        """Get link by id"""
        result = await self.session.get(LinkDB, id)
        if not result:
            return None
        
        return EvolutionLink(
            id=result.id,
            from_id=result.from_id,
            to_id=result.to_id,
            type=result.type
        )

    async def list_all(self) -> List[EvolutionLink]:
        """Get all links"""
        stmt = select(LinkDB)
        result = await self.session.execute(stmt)
        links = result.scalars().all()
        
        return [
            EvolutionLink(
                id=l.id,
                from_id=l.from_id,
                to_id=l.to_id,
                type=l.type
            )
            for l in links
        ]

    async def list_by_from_id(self, from_id: int) -> List[EvolutionLink]:
        """Get links starting from specific mechanic"""
        stmt = select(LinkDB).where(LinkDB.from_id == from_id)
        result = await self.session.execute(stmt)
        links = result.scalars().all()
        
        return [
            EvolutionLink(
                id=l.id,
                from_id=l.from_id,
                to_id=l.to_id,
                type=l.type
            )
            for l in links
        ]

    async def delete(self, id: int) -> bool:
        """Delete link by id"""
        db_link = await self.session.get(LinkDB, id)
        if not db_link:
            return False
        
        await self.session.delete(db_link)
        await self.session.commit()
        return True
