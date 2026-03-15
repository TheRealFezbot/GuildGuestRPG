from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.core.enums import ItemType, ItemRarity, ClassType

class InventoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inventory_id: UUID
    id: UUID
    name: str
    type: ItemType
    rarity: ItemRarity
    class_type: ClassType | None
    attack_bonus: int
    defense_bonus: int
    hp_bonus: int
    buy_price: int
    sell_price: int
    level_requirement: int
    equipped_slot: ItemType | None

