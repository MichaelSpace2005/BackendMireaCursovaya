from dataclasses import dataclass
from typing import Optional


@dataclass
class EvolutionLink:
    """Domain entity for link between mechanics"""
    id: Optional[int]
    from_id: int
    to_id: int
    type: str 

    def __post_init__(self):
        """Validate link"""
        if self.from_id == self.to_id:
            raise ValueError("Link cannot point to itself")
        if not self.type or len(self.type.strip()) == 0:
            raise ValueError("Link type cannot be empty")
