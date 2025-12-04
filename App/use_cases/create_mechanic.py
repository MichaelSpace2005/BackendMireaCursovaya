from typing import Protocol
from app.entities.mechanic import GameMechanic

class IMechanicRepo(Protocol):
    async def create(self, mechanic: GameMechanic) -> GameMechanic: ...
    async def get_by_id(self, id: int) -> GameMechanic | None: ...

class CreateMechanicUseCase:
    def __init__(self, repo: IMechanicRepo):
        self.repo = repo

    async def execute(self, mechanic: GameMechanic) -> GameMechanic:
        # basic validation
        if not mechanic.name or len(mechanic.name.strip()) == 0:
            raise ValueError("Mechanic name is required")
        return await self.repo.create(mechanic)