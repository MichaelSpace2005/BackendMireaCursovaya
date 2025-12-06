from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.link import EvolutionLink


class ILinkRepository(ABC):
    """Interface for link repository"""

    @abstractmethod
    async def create(self, link: EvolutionLink) -> EvolutionLink:
        """Create new link"""
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[EvolutionLink]:
        """Get link by id"""
        pass

    @abstractmethod
    async def list_all(self) -> List[EvolutionLink]:
        """Get all links"""
        pass

    @abstractmethod
    async def list_by_from_id(self, from_id: int) -> List[EvolutionLink]:
        """Get all links from mechanic"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete link by id"""
        pass
