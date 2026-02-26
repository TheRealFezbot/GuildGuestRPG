from sqlalchemy import Column, ForeignKey, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class MonsterDrops(Base):
    __tablename__ = "monster_drops"
    __table_args__ = (
        UniqueConstraint("monster_id", "item_id", name="uq_monster_item"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monster_id = Column(UUID(as_uuid=True), ForeignKey("monsters.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    drop_chance = Column(Float, nullable=False)