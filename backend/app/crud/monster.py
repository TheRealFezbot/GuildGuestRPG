from sqlalchemy.orm import Session

from app.models.monster import Monster
from app.models.monster_progress import MonsterProgress

def get_monsters_for_zone(db: Session, zone_id: str, character_id: str):
    monsters = db.query(Monster, MonsterProgress)\
        .outerjoin(MonsterProgress, (MonsterProgress.monster_id == Monster.id) & (MonsterProgress.character_id == character_id))\
        .filter(Monster.zone_id == zone_id).order_by(Monster.order_in_zone).all()
    result = []
    prev_highest = 0
    for monster, progress in monsters:
        if monster.order_in_zone == 1:
            is_unlocked = True
        else:
            is_unlocked = prev_highest >= 3
            
        monster_data = {k: v for k, v in monster.__dict__.items() if not k.startswith("_")}
        monster_data["highest_level_beaten"] = progress.highest_level_beaten if progress else 0
        monster_data["total_kills"] = progress.total_kills if progress else 0
        monster_data["is_unlocked"] = is_unlocked
        result.append(monster_data)

        prev_highest = monster_data["highest_level_beaten"]
    
    return result