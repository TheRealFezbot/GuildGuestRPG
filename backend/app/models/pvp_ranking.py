from sqlalchemy import Column, ForeignKey, Integer, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.database import Base

class PvpRanking(Base):
    __tablename__ = "pvp_ranking"
    __table_args__ = (
        CheckConstraint("rating >= 0", name="check_rating_non_negative"),
    )

    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), primary_key=True)
    rating = Column(Integer, default=1000, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)