from app.entities.mechanic import GameMechanic
from app.interfaces.repos.mechanic_repo import IMechanicRepository


class CreateMechanicUseCase:
    """Use case for creating a mechanic"""
    
    def __init__(self, mechanic_repo: IMechanicRepository):
        self.mechanic_repo = mechanic_repo
    
    async def execute(self, mechanic: GameMechanic) -> GameMechanic:
        """Execute mechanic creation"""
        if not mechanic.name or not mechanic.name.strip():
            raise ValueError("Mechanic name cannot be empty")
        
        return await self.mechanic_repo.create(mechanic)
