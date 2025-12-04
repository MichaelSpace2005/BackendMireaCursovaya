from abc import ABC, abstractmethod
from app.entities.link import EvolutionLink
from typing import List, Optional

class ILinkRepository(ABC):
    @abstractmethod
    async def create(self, link: EvolutionLink) -> EvolutionLink: ...
    @abstractmethod
    async def list_links_from(self, from_id: int) -> List[EvolutionLink]: ...
    @abstractmethod
    async def list_links(self) -> List[EvolutionLink]: ...