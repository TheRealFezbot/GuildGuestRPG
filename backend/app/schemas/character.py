from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID

from app.models.character import ClassType

class CharacterCreate(BaseModel):
    name: str
    class_type: ClassType

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty.")
        return v.strip()

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
    power_level: int
    stamina: int
    created_at: datetime

class CharacterPublic(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    name: str
    class_type: ClassType
    level: int
    power_level: int