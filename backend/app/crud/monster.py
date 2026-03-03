from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.monster import Monster
from app.models.monster_level import MonsterLevel
from app.models.monster_progress import MonsterProgress

def get_monsters_for_zone(db: Session, zone_id: str, character_id: str):
    monsters = db.query(Monster, MonsterProgress)\
        .outerjoin(MonsterProgress, (MonsterProgress.monster_id == Monster.id) & (MonsterProgress.character_id == character_id))\
        .filter(Monster.zone_id == zone_id).order_by(Monster.order_in_zone).all()
    result = []
    prev_highest = 0
    for monster, progress in monsters:
        levels_list = get_monster_levels(db, monster.id)
        if monster.order_in_zone == 1:
            is_unlocked = True
        else:
            is_unlocked = prev_highest >= 3
            
        monster_data = {k: v for k, v in monster.__dict__.items() if not k.startswith("_")}
        monster_data["highest_level_beaten"] = progress.highest_level_beaten if progress else 0
        monster_data["total_kills"] = progress.total_kills if progress else 0
        monster_data["is_unlocked"] = is_unlocked
        monster_data["levels"] = levels_list
        result.append(monster_data)

        prev_highest = monster_data["highest_level_beaten"]
    
    return result

def get_monster_levels(db: Session, monster_id: str):
    return db.query(MonsterLevel)\
        .filter(MonsterLevel.monster_id == monster_id)\
        .order_by(MonsterLevel.level).all()

def get_monster_by_id(db: Session, monster_id: str):
    return db.query(Monster).filter(Monster.id == monster_id).first()
    
def get_validated_zone_monster(db: Session, monster_id: str, character_id: str, level: int):
    monster = get_monster_by_id(db, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    
    zone_monsters = get_monsters_for_zone(db, str(monster.zone_id), character_id)
    zone_monster = next((m for m in zone_monsters if m["id"] == monster.id), None)

    if not zone_monster or not zone_monster["is_unlocked"]:
        raise HTTPException(status_code=403, detail="Monster is locked")
    if level < 1 or level > zone_monster["highest_level_beaten"] + 1:
        raise HTTPException(status_code=400, detail="Level not available")
    
    return zone_monster
