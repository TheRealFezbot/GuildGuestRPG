import uuid
from sqlalchemy.orm import Session

from app.models.zone import Zone
from app.core.enums import ClassType
from app.core.constants import BASE_STATS
from app.models.character import Character
from app.core.game import calculate_power_level
from app.models.zone_progress import ZoneProgress



def create_character(db: Session, user_id: str, name: str, class_type: ClassType):
    hp = BASE_STATS[class_type]["hp"]
    attack = BASE_STATS[class_type]["attack"]
    defense = BASE_STATS[class_type]["defense"]
    
    
    char_id = uuid.uuid4()
    character = Character(
        id = char_id,
        user_id = user_id,
        name = name,
        class_type = class_type,
        hp = hp,
        max_hp = hp,
        attack = attack,
        defense = defense,
        power_level = calculate_power_level(hp, attack, defense) 
    )
    zone = db.query(Zone).filter(Zone.order == 1).first()
    if zone:
        zone_progress = ZoneProgress(
            character_id = character.id,
            zone_id = zone.id,
            is_unlocked = True,
        )
        db.add(zone_progress)
    db.add(character)
    db.commit()
    db.refresh(character)
    return character

def get_character_by_id(db: Session, char_id: str):
    return db.query(Character).filter(Character.id == char_id).first()

def get_character_by_name(db: Session, name: str):
    return db.query(Character).filter(Character.name == name).first()

def get_character_by_user_id(db: Session, user_id: str):
    return db.query(Character).filter(Character.user_id == user_id).first()

def get_character_by_user_id_locked(db: Session, user_id: str):
    return db.query(Character).filter(Character.user_id == user_id).with_for_update().first()