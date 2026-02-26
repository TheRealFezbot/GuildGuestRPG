from sqlalchemy import Column, ForeignKey, Float, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class MonsterDrops(Base):
    __tablename__ = "monster_drops"
    __table_args__ = (
        UniqueConstraint("monster_id", "item_id", name="uq_monster_item"),
        CheckConstraint("drop_chance >= 0", name="check_drop_chance_non_negative"),
        CheckConstraint("drop_chance <= 1", name="check_drop_chance_non_exceeding"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monster_id = Column(UUID(as_uuid=True), ForeignKey("monsters.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    drop_chance = Column(Float, nullable=False)