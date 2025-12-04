from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repos.link_repo import ILinkRepository
from app.entities.link import EvolutionLink
from app.infra.database.models import LinkDB

class LinkRepository(ILinkRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, link: EvolutionLink) -> EvolutionLink:
        db = LinkDB(from_id=link.from_id, to_id=link.to_id, type=link.type)
        self.session.add(db)
        await self.session.commit()
        await self.session.refresh(db)
        return EvolutionLink(id=db.id, from_id=db.from_id, to_id=db.to_id, type=db.type)

    async def list_links_from(self, from_id: int) -> List[EvolutionLink]:
        q = await self.session.execute(select(LinkDB).where(LinkDB.from_id == from_id))
        rows = q.scalars().all()
        return [EvolutionLink(id=r.id, from_id=r.from_id, to_id=r.to_id, type=r.type) for r in rows]

    async def list_links(self) -> List[EvolutionLink]:
        q = await self.session.execute(select(LinkDB))
        rows = q.scalars().all()
        return [EvolutionLink(id=r.id, from_id=r.from_id, to_id=r.to_id, type=r.type) for r in rows]