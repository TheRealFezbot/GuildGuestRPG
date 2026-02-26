from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.enums import ClassType
from app.core.database import Base
import uuid

class Character(Base):
    __tablename__ = "characters"

    __table_args__ = (
        CheckConstraint("gold >= 0", name="check_gold_non_negative"),
        CheckConstraint("stamina >= 0", name="check_stamina_non_negative"),
        CheckConstraint("stamina <= 100", name="check_stamina_max"),
        CheckConstraint("hp >= 0", name="check_hp_non_negative"),
        CheckConstraint("hp <= max_hp", name="check_hp_max"),
        CheckConstraint("pvp_tokens >= 0", name="check_pvp_tokens_non_negative"),
        CheckConstraint("pvp_rating >= 0", name="check_pvp_rating_non_negative"),
        CheckConstraint("level >= 1", name="check_level_min"),
        CheckConstraint("xp >= 0", name="check_xp_non_negative"),
        # TODO: Add a max_level constraint once max level has been decided
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    class_type = Column(Enum(ClassType), nullable=False)
    level = Column(Integer, default=1, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    gold = Column(Integer, default=100, nullable=False)
    hp = Column(Integer, nullable=False)
    max_hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    stamina = Column(Integer, default=100, nullable=False)
    stamina_updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    pvp_tokens = Column(Integer, default=3, nullable=False)
    pvp_tokens_reset_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    pvp_rating = Column(Integer, default=1000, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)