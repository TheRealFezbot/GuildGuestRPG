from sqlalchemy import Column, Integer, Float, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class MonsterLevel(Base):
    __tablename__ = "monster_levels"
    __table_args__ = (
        CheckConstraint("level >= 1", name="check_level_min"),
        CheckConstraint("level <= 5", name="check_level_max"),
        UniqueConstraint("monster_id", "level", name="uq_check_monster_level")
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monster_id = Column(UUID(as_uuid=True), ForeignKey("monsters.id"), nullable=False)
    level = Column(Integer, nullable=False)
    hp_multiplier = Column(Float, nullable=False)
    attack_multiplier = Column(Float, nullable=False)
    defense_multiplier = Column(Float, nullable=False)
    xp_multiplier = Column(Float, nullable=False)
    gold_multiplier = Column(Float, nullable=False)
    drop_chance_bonus = Column(Float, nullable=False)