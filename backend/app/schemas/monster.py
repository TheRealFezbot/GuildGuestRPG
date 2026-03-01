from pydantic import BaseModel
from uuid import UUID

class MonsterWithProgressResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    zone_id: UUID
    name: str
    base_hp: int
    base_attack: int
    base_defense: int
    base_xp_reward: int
    base_gold_min: int
    base_gold_max: int
    order_in_zone: int
    is_zone_boss: bool
    highest_level_beaten: int = 0
    total_kills: int = 0
    is_unlocked: bool = False