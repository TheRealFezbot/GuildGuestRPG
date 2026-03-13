from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.enums import ItemRarity, ItemType, ClassType
from app.core.database import Base
import uuid

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(ItemType), nullable=False)
    rarity = Column(Enum(ItemRarity), nullable=False)
    attack_bonus = Column(Integer, default=0, nullable=False)
    defense_bonus = Column(Integer, default=0, nullable=False)
    hp_bonus = Column(Integer, default=0, nullable=False)
    buy_price = Column(Integer, default=0, nullable=False)
    sell_price = Column(Integer, nullable=False)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"))
    level_requirement = Column(Integer, default=0, nullable=False)
    class_type = Column(Enum(ClassType))