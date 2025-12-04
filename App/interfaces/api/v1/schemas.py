from pydantic import BaseModel, Field
from typing import Optional, List, Any

class MechanicDTO(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    year: Optional[int] = None

class LinkDTO(BaseModel):
    id: Optional[int] = None
    from_id: int
    to_id: int
    type: str

class TreeResponse(BaseModel):
    root: Any