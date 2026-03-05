from sqlalchemy.orm import Session

from app.models.zone import Zone
from app.models.zone_progress import ZoneProgress

def get_zones_for_character(db: Session, character_id: str):
    zones = db.query(Zone, ZoneProgress)\
        .outerjoin(ZoneProgress, (ZoneProgress.zone_id == Zone.id) & (ZoneProgress.character_id == character_id))\
        .order_by(Zone.order)\
        .all()
    result = []
    for zone, progress in zones:
        zone_data = {k: v for k, v in zone.__dict__.items() if not k.startswith("_")}
        zone_data["is_unlocked"] = progress.is_unlocked if progress else False
        result.append(zone_data)
    
    return result

def get_zone_progress(db: Session, zone_id: str, character_id: str):
    return db.query(ZoneProgress).filter(ZoneProgress.zone_id == zone_id, ZoneProgress.character_id == character_id).first()

def get_zone_by_id(db: Session, zone_id: str):
    return db.query(Zone).filter(Zone.id == zone_id).first()

def get_next_zone(db: Session, zone_id: str):
    current_zone = get_zone_by_id(db, zone_id)
    return db.query(Zone).filter(Zone.order == current_zone.order + 1).first()