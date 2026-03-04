from sqlalchemy.orm import Session

from app.models.monster_progress import MonsterProgress
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

def save_combat_result(
        db: Session, 
        character_id: str, 
        monster_id: str, 
        level_beaten: int, 
        combat_result: CombatResult, 
        result: dict):
    _update_monster_progress(db, character_id, monster_id, level_beaten, combat_result == CombatResult.win)
    _create_combat_log(db, character_id, monster_id, level_beaten, combat_result, result)
    db.commit()
