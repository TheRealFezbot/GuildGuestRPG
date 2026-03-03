from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.character import get_character_by_user_id_locked, apply_combat_result
from app.crud.monster import get_validated_zone_monster
from app.core.dependencies import get_current_user
from app.services.combat import simulate_combat
from app.crud.combat import save_combat_result
from app.core.game import get_current_stamina
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

    current_stamina = get_current_stamina(character)
    stamina_cost = 5 # TODO: 10 for boss
    if current_stamina < stamina_cost:
        raise HTTPException(status_code=400, detail="Not enough stamina")

    zone_monster = get_validated_zone_monster(db, request.monster_id, character.id, request.level)
    
    result = simulate_combat(character, zone_monster, request.level)
    apply_combat_result(character, current_stamina, stamina_cost, result)

    combat_result = CombatResult.win if result["winner"] == "player" else CombatResult.lose
    save_combat_result(db, character.id, zone_monster["id"], request.level, combat_result, result)

    return result
