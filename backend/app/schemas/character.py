from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID

from app.core.constants import MIN_CHARACTER_NAME_LENGTH, MAX_CHARACTER_NAME_LENGTH
from app.models.character import ClassType
from app.core.security import validate_name

class CharacterCreate(BaseModel):
    name: str
    class_type: ClassType

    @field_validator("name")
    @classmethod
    def validate_character_name(cls, v):
        return validate_name(v, MIN_CHARACTER_NAME_LENGTH, MAX_CHARACTER_NAME_LENGTH, "Character Name")

class CharacterResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    name: str
    class_type: ClassType
    level: int
    xp: int
    gold: int
    hp: int
    max_hp: int
    attack: int
    defense: int
    crit_bonus: float
    dodge_bonus: float
    power_level: int
    stamina: int
    stamina_updated_at: datetime
    created_at: datetime

class CharacterPublic(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    name: str
    class_type: ClassType
    level: int
    power_level: int