from sqlalchemy import Column, ForeignKey, Integer, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.database import Base
import uuid

class PvpMatches(Base):
    __tablename__ = "pvp_matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenger_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    defender_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    winner_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    combat_text = Column(JSON, nullable=False)
    challenger_damage = Column(Integer, nullable=False, default=0)
    defender_damage = Column(Integer, nullable=False, default=0)
    challenger_rating_change = Column(Integer, nullable=False)
    defender_rating_change = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))