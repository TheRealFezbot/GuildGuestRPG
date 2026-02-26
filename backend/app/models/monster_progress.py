from sqlalchemy import Column, Integer, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class MonsterProgress(Base):
    __tablename__ = "monster_progress"
    __table_args__ = (
        CheckConstraint("highest_level_beaten >= 0", name="check_level_beaten_min"),
        CheckConstraint("highest_level_beaten <= 5", name="check_level_beaten_max"),
        UniqueConstraint("character_id", "monster_id", name="uq_character_monster")
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    monster_id = Column(UUID(as_uuid=True), ForeignKey("monsters.id"), nullable=False)
    highest_level_beaten = Column(Integer, default=0, nullable=False)
    total_kills = Column(Integer, default=0, nullable=False)