from sqlalchemy import Column, String, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class Zone(Base):
    __tablename__ = "zones"
    __table_args__ = (
        CheckConstraint("order >= 1", name="check_order_min"),
        CheckConstraint("order <= 4", name="check_order_max"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    recommended_level_min = Column(Integer, nullable=False)
    recommended_level_max = Column(Integer, nullable=False)