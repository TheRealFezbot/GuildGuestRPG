from pydantic import BaseModel

class FightRequest(BaseModel):
    monster_id: str
    level: int