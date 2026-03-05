from sqlalchemy.orm import Session

from app.crud.zone import get_next_zone, get_zone_progress
from app.models.monster_progress import MonsterProgress
from app.core.constants import ZONE_UNLOCK_THRESHOLD
from app.models.zone_progress import ZoneProgress
from app.crud.monster import get_monster_by_id
from app.models.combat_logs import CombatLogs
from app.core.enums import CombatResult

def _update_monster_progress(db: Session, character_id: str, monster_id: str, level_beaten: int, won: bool):
    progress = db.query(MonsterProgress).filter(
        MonsterProgress.character_id == character_id,
        MonsterProgress.monster_id == monster_id
    ).first()

    if won:
        if progress:
            progress.total_kills += 1
            if level_beaten > progress.highest_level_beaten:
                progress.highest_level_beaten = level_beaten
        else:
            db.add(MonsterProgress(
                character_id=character_id, 
                monster_id=monster_id, 
                highest_level_beaten=level_beaten, 
                total_kills=1))
    elif not progress:
        # create an empty progress row on first attempt so losses can be tracked later
        db.add(MonsterProgress(character_id=character_id, monster_id=monster_id))

def _create_combat_log(db: Session, character_id: str, monster_id: str, level: int, combat_result: CombatResult, result: dict):
    db.add(CombatLogs(
        character_id=character_id,
        monster_id=monster_id,
        monster_level=level,
        result=combat_result,
        xp_gained=result["xp_gained"],
        gold_gained=result["gold_gained"],
        turns_taken=result["turns_taken"],
        combat_text=result["combat_text"],
        potions_used=[],
        damage_dealt=result["damage_dealt"],
        damage_taken=result["damage_taken"],
        )
    )

def _unlock_next_zone(db: Session, character_id: str, monster_id: str, level_beaten: int):
    monster = get_monster_by_id(db, monster_id)
    if monster.is_zone_boss and level_beaten >= ZONE_UNLOCK_THRESHOLD:
        next_zone = get_next_zone(db, monster.zone_id)
        if next_zone:
            next_zone_progress = get_zone_progress(db, next_zone.id, character_id)
            if next_zone_progress:
                next_zone_progress.is_unlocked = True
            else:
                db.add(ZoneProgress(zone_id=next_zone.id, character_id=character_id, is_unlocked=True))


def save_combat_result(
        db: Session, 
        character_id: str, 
        monster_id: str, 
        level_beaten: int, 
        combat_result: CombatResult, 
        result: dict):
    _update_monster_progress(db, character_id, monster_id, level_beaten, combat_result == CombatResult.win)
    _create_combat_log(db, character_id, monster_id, level_beaten, combat_result, result)
    # checks if zone should be unlocked and if so unlocks it
    if combat_result == CombatResult.win:
        _unlock_next_zone(db, character_id, monster_id, level_beaten)
    db.commit()
