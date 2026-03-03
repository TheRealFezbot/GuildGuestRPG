import uuid
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.zone import Zone
from app.core.enums import ClassType
from app.core.constants import BASE_STATS, STAT_GROWTH
from app.models.character import Character
from app.core.game import calculate_power_level, xp_for_next_level
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

def apply_combat_result(character: Character, current_stamina: int, stamina_cost: int, result: dict):
    now = datetime.now(timezone.utc)
    character.stamina = current_stamina - stamina_cost
    character.stamina_updated_at = now
    character.gold += result["gold_gained"]
    character.xp += result["xp_gained"]
    character.hp = character.max_hp
    level_up(character)

def level_up(character: Character):
    xp_needed = xp_for_next_level(character.level)
    while character.xp >= xp_needed:
        character.xp -= xp_needed
        character.level += 1
        character.max_hp += STAT_GROWTH[character.class_type]["max_hp"]
        character.hp = character.max_hp
        character.attack += STAT_GROWTH[character.class_type]["attack"]
        character.defense += STAT_GROWTH[character.class_type]["defense"]
        character.power_level = calculate_power_level(character.max_hp, character.attack, character.defense)
