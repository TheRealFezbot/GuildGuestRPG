from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.enums import CombatResult
from app.core.database import Base
import uuid

class CombatLogs(Base):
    __tablename__ = "combat_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    monster_id = Column(UUID(as_uuid=True), ForeignKey("monsters.id"), nullable=False)
    monster_level = Column(Integer, nullable=False)
    result = Column(Enum(CombatResult), nullable=False)
    xp_gained = Column(Integer, nullable=False)
    gold_gained = Column(Integer, nullable=False)
    item_dropped_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    turns_taken = Column(Integer, nullable=False)
    combat_text = Column(JSON, nullable=False)
    potions_used = Column(JSON, nullable=False)
    damage_dealt = Column(Integer, nullable=False, default=0)
    damage_taken = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)