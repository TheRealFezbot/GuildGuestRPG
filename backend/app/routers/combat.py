from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.crud.monster import get_monster_by_id, get_monsters_for_zone
from app.core.game import calculate_power_level, xp_for_next_level
from app.crud.character import get_character_by_user_id_locked
from app.core.dependencies import get_current_user
from app.services.combat import simulate_combat
from app.crud.combat import save_combat_result
from app.schemas.combat import FightRequest
from app.core.enums import CombatResult
from app.core.database import get_db
from app.models.user import User


router = APIRouter(prefix="/combat", tags=["combat"])

@router.post("/fight")
async def fight(request: FightRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id_locked(db, current_user.id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # TODO: calculate stamina function
    now = datetime.now(timezone.utc)
    elapsed_minutes = (now - character.stamina_updated_at.replace(tzinfo=timezone.utc)).total_seconds() / 60
    regen = int(elapsed_minutes / 3)
    current_stamina = min(100, character.stamina + regen)

    stamina_cost = 5 # TODO: 10 for boss
    if current_stamina < stamina_cost:
        raise HTTPException(status_code=400, detail="Not enough stamina")
    
    # TODO: Create fetch monster function
    monster = get_monster_by_id(db, request.monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    
    zone_monsters = get_monsters_for_zone(db, str(monster.zone_id), character.id)
    zone_monster = next((m for m in zone_monsters if m["id"] == monster.id), None)

    if not zone_monster or not zone_monster["is_unlocked"]:
        raise HTTPException(status_code=403, detail="Monster is locked")
    if request.level < 1 or request.level > zone_monster["highest_level_beaten"] + 1:
        raise HTTPException(status_code=400, detail="Level not available")
    
    # Simulate combat
    result = simulate_combat(character, zone_monster, request.level)
    
    # TODO: Create Apply_result function and level_up function
    character.stamina = current_stamina - stamina_cost
    character.stamina_updated_at = now
    character.gold += result["gold_gained"]
    character.xp += result["xp_gained"]
    character.hp = character.max_hp
    
    xp_needed = xp_for_next_level(character.level)
    while character.xp >= xp_needed:
        character.xp -= xp_needed
        character.level += 1
        # TODO: grow stats on level up
        character.power_level = calculate_power_level(character.max_hp, character.attack, character.defense)

    # Save Combat Result
    combat_result = CombatResult.win if result["winner"] == "player" else CombatResult.lose
    save_combat_result(db, character.id, zone_monster["id"], request.level, combat_result, result)

    return result
