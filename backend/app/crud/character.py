from sqlalchemy.orm import Session

from app.core.enums import ClassType
from app.models.character import Character

BASE_STATS = {
    ClassType.warrior: {
        "hp": 120,
        "attack": 10,
        "defense": 8,
    },
    ClassType.mage: {
        "hp": 80,
        "attack": 15,
        "defense": 4,
    },
    ClassType.rogue: {
        "hp": 100,
        "attack": 12,
        "defense": 5,
    },
    ClassType.ranger: {
        "hp": 100,
        "attack": 11,
        "defense": 6,
    },
}

def create_character(db: Session, user_id: str, name: str, class_type: ClassType):
    hp = BASE_STATS[class_type]["hp"]
    attack = BASE_STATS[class_type]["attack"]
    defense = BASE_STATS[class_type]["defense"]
    
    character = Character(
        user_id = user_id,
        name = name,
        class_type = class_type,
        hp = hp,
        max_hp = hp,
        attack = attack,
        defense = defense,
        power_level = 10 + attack + defense + hp / 2 
    )
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