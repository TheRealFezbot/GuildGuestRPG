from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.enums import PotionType
from app.core.database import Base
import uuid

class Potion(Base):
    __tablename__ = "potions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(PotionType), nullable=False)
    value = Column(Integer, nullable=False)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"))
    buy_price = Column(Integer, default=0, nullable=False)
    sell_price = Column(Integer, nullable=False)