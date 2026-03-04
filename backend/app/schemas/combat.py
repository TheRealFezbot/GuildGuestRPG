from pydantic import BaseModel

class FightRequest(BaseModel):
    monster_id: str
    level: int

class CombatResultResponse(BaseModel):
    winner: str
    xp_gained: int
    gold_gained: int
    item_dropped_id: str | None
    turns_taken: int
    damage_dealt: int
    damage_taken: int
    combat_text: list[str]