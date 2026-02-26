from sqlalchemy import Column, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class ZoneProgress(Base):
    __tablename__ = "zone_progress"
    __table_args__ = (
        UniqueConstraint("character_id", "zone_id", name="uq_check_character_zone"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)
    is_unlocked = Column(Boolean, default=False, nullable=False)