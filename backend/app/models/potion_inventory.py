from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class PotionInventory(Base):
    __tablename__ = "potion_inventory"
    __table_args__ = (
        UniqueConstraint("character_id", "potion_id", name="uq_character_potion"),
        CheckConstraint("quantity >= 0", name="check_quantity_non_negative")
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    potion_id = Column(UUID(as_uuid=True), ForeignKey("potions.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)