from sqlalchemy import Column, ForeignKey, Enum, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.enums import ItemType
from datetime import datetime, timezone
from app.core.database import Base
import uuid

class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (
        UniqueConstraint("character_id", "equipped_slot"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    equipped_slot = Column(Enum(ItemType))
    acquired_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
