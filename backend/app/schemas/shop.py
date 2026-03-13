from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.core.enums import ItemType, ItemRarity, ClassType

class ShopItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    listing_id: UUID
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
    stock: int | None

class BuyResponse(BaseModel):
    message: str
    item_name: str
    gold_remaining: int