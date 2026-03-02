from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.database import get_db
from app.schemas.zone import ZoneResponse
from app.crud.zone import get_zones_for_character, get_zone_progress
from app.crud.monster import get_monsters_for_zone, get_monster_by_id
from app.core.dependencies import get_current_user
from app.crud.character import get_character_by_user_id
from app.schemas.monster import MonsterWithProgressResponse

router = APIRouter(prefix="/zones", tags=["zones"])

@router.get("/", response_model=list[ZoneResponse])
async def get_zones(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    return get_zones_for_character(db, character.id)

@router.get("/monsters/{monster_id}", response_model=MonsterWithProgressResponse)
async def get_monster(monster_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    monster = get_monster_by_id(db, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Couldn't find monster")
    zone_monsters = get_monsters_for_zone(db, str(monster.zone_id), character.id)
    zone_monster = next((m for m in zone_monsters if m["id"] == monster.id), None)
    if not zone_monster:
        raise HTTPException(status_code=404, detail="Couldn't find monster")

    return zone_monster

@router.get("/{zone_id}/monsters", response_model=list[MonsterWithProgressResponse])
async def get_monsters(zone_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    zone_progress = get_zone_progress(db, zone_id, character.id)

    if not zone_progress or not zone_progress.is_unlocked:
        raise HTTPException(status_code=403, detail="You don't have access to this zone")
    
    return get_monsters_for_zone(db, zone_id, character.id)
