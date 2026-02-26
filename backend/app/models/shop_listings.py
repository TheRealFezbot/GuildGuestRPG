from sqlalchemy import Column, ForeignKey, Integer, Boolean, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class ShopListings(Base):
    __tablename__ = "shop_listings"
    __table_args__ = (
        CheckConstraint("(item_id IS NOT NULL AND potion_id IS NULL) OR (item_id IS NULL AND potion_id IS NOT NULL)", name="check_item_or_potion"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    potion_id = Column(UUID(as_uuid=True), ForeignKey("potions.id"))
    stock = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)