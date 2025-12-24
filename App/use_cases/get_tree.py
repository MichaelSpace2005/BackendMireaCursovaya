from dataclasses import dataclass
from typing import List

from app.entities.mechanic import GameMechanic
from app.entities.link import EvolutionLink
from app.interfaces.repos.mechanic_repo import IMechanicRepository
from app.interfaces.repos.link_repo import ILinkRepository


@dataclass
class MechanicTree:
    """Tree structure for mechanic"""
    mechanic: GameMechanic
    children: List["MechanicTree"]


class GetMechanicTreeUseCase:
    """Use case for getting mechanic evolution tree"""
    
    def __init__(self, mechanic_repo: IMechanicRepository, link_repo: ILinkRepository):
        self.mechanic_repo = mechanic_repo
        self.link_repo = link_repo
    
    async def execute(self, mechanic_id: int) -> MechanicTree:
        """Execute tree building"""
        mechanic = await self.mechanic_repo.get_by_id(mechanic_id)
        if not mechanic:
            raise ValueError("Mechanic not found")
        
        tree = await self._build_tree(mechanic_id, visited=set())
        return tree
    
    async def _build_tree(self, mechanic_id: int, visited: set) -> MechanicTree:
        """Recursively build mechanic tree"""
        if mechanic_id in visited:
            mechanic = await self.mechanic_repo.get_by_id(mechanic_id)
            return MechanicTree(mechanic=mechanic, children=[])
        
        visited.add(mechanic_id)
        
        mechanic = await self.mechanic_repo.get_by_id(mechanic_id)
        links = await self.link_repo.list_by_from_id(mechanic_id)
        
        children = []
        for link in links:
            child_tree = await self._build_tree(link.to_id, visited.copy())
            children.append(child_tree)
        
        return MechanicTree(mechanic=mechanic, children=children)
