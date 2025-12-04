from abc import ABC, abstractmethod
from app.entities.mechanic import GameMechanic
from typing import List, Optional

class IMechanicRepository(ABC):
    @abstractmethod
    async def create(self, mechanic: GameMechanic) -> GameMechanic: ...
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[GameMechanic]: ...
    @abstractmethod
    async def list_all(self) -> List[GameMechanic]: ...