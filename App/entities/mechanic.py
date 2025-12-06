from dataclasses import dataclass
from typing import Optional


@dataclass
class GameMechanic:
    """Domain entity for game mechanic"""
    id: Optional[int]
    name: str
    description: Optional[str] = None
    year: Optional[int] = None

    def __post_init__(self):
        """Validate mechanic"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Mechanic name cannot be empty")
