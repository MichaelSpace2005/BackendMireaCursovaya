from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class GameMechanic:
    id: Optional[int]
    name: str
    description: Optional[str] = None