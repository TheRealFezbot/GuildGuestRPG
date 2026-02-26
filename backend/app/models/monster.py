from sqlalchemy import Column, Boolean, String, Integer, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class Monster(Base):
    __tablename__ = "monsters"
    __table_args__ = (
        CheckConstraint("order_in_zone >= 1", name="check_order_in_zone_min"),
        CheckConstraint("order_in_zone <= 4", name="check_order_in_zone_max"),
        CheckConstraint("base_gold_min <= base_gold_max", name="check_base_gold_non_exceeding"),
        UniqueConstraint("zone_id", "order_in_zone", name="uq_monster_zone_order")
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    name = Column(String, nullable=False)
    base_hp = Column(Integer, nullable=False)
    base_attack = Column(Integer, nullable=False)
    base_defense = Column(Integer, nullable=False)
    base_xp_reward = Column(Integer, nullable=False)
    base_gold_min = Column(Integer, nullable=False)
    base_gold_max = Column(Integer, nullable=False)
    order_in_zone = Column(Integer, nullable=False)
    is_zone_boss = Column(Boolean, default=False, nullable=False)