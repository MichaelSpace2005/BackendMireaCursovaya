from dataclasses import dataclass
from typing import Optional

@dataclass
class EvolutionLink:
    id: Optional[int]
    from_id: int
    to_id: int
    type: str  # e.g. "inspired_by", "direct_descendant", "variant"