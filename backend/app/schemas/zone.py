from pydantic import BaseModel
from uuid import UUID

class ZoneResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    name: str
    description: str
    order: int
    recommended_level_min: int
    recommended_level_max: int
    is_unlocked: bool = False