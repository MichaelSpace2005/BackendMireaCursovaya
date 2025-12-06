from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.mechanic import GameMechanic


class IMechanicRepository(ABC):
    """Interface for mechanic repository"""

    @abstractmethod
    async def create(self, mechanic: GameMechanic) -> GameMechanic:
        """Create new mechanic"""
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[GameMechanic]:
        """Get mechanic by id"""
        pass

    @abstractmethod
    async def list_all(self) -> List[GameMechanic]:
        """Get all mechanics"""
        pass

    @abstractmethod
    async def update(self, mechanic: GameMechanic) -> GameMechanic:
        """Update existing mechanic"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete mechanic by id"""
        pass
